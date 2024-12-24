import hashlib
import uuid
import mysql.connector
from data.db import Db

class User:
    def __init__(self, name: str, email: str, password:str, login:str=None ):
        self.name = name
        self.email = email
        self.password = password
        self.login = login if login is not None else email

class UserDao:
    def __init__(self, db: Db): self.__db = db

    def create_tables(self):
        connection = self.__db.get_connection()
        sql = """CREATE TABLE users (
        `user_id` CHAR(36) PRIMARY KEY DEFAULT( UUID()),
        `user_name` VARCHAR(128) NOT NULL,
        `user_email` VARCHAR(256) NOT NULL
        ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
        """
        connection.cursor().execute(sql)

        sql = """CREATE TABLE user_access (
                `ua_id` CHAR(36) PRIMARY KEY DEFAULT( UUID()),
                `user_id` CHAR(36) NOT NULL,
                `ua_login` VARCHAR(256) NOT NULL,
                `ua_hash` VARCHAR(32) NOT NULL,
                `ua_salt` VARCHAR(16) NOT NULL
                ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
                """
        connection.cursor().execute(sql)
        connection.commit()

    def get_all_users(self):
        with DbContext() as context: return context.session.query(User).all()

    def is_login_free(self, login: str) -> bool:
        conn = self.__db.get_connection()
        sql = "SELECT COUNT(*) FROM users_access ua WHERE ua.ua_login = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(login))
            row = cursor.fetchone()
        conn.commit()
        return row[0] == 0

    def add_user(self, user: User):
        conn = self.__db.get_connection()
        salt = hashlib.md5(user.password.encode()).hexdigest()[:16]
        password_hash = hashlib.md5(user.password.encode()).hexdigest()

        try:
            sql = "SELECT COUNT(*) FROM user_access WHERE ua_login = %s"
            with conn.cursor() as cursor:
                cursor.execute(sql, (user.login,))
                count = cursor.fetchone()[0]
            if count > 0: raise ValueError(f"Login '{user.login}' is already in use.")

            user_id = str(uuid.uuid4())
            sql = "INSERT INTO users (`user_id`, `user_name`, `user_email`) VALUES (%s, %s, %s)"
            with conn.cursor() as cursor: cursor.execute(sql, (user_id, user.name, user.email))

            sql = "INSERT INTO user_access (`user_id`, `ua_login`, `ua_hash`, `ua_salt`) VALUES (%s, %s, %s, %s)"
            with conn.cursor() as cursor: cursor.execute(sql, (user_id, user.login, password_hash, salt))
            conn.commit()

        except mysql.connector.Error as err:
            conn.rollback()  
            raise err