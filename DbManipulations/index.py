import mysql.connector
import json

class Db:
    def __init__(self, config):
        if isinstance(config, dict):
            if 'db' in config:  self.config = config['db']
            else: self.config = config
        elif isinstance(config, str):
            try:
                with open(config, 'r') as file:
                    self.config = json.load(file)
                    if 'db' in self.config: self.config = self.config['db']
            except FileNotFoundError: raise ValueError(f"Файл настройки '{config}' не найден.")
            except json.JSONDecodeError: raise ValueError(f"Ошибка декодирования JSON из файла настройки '{config}'.")
        else: raise TypeError("Параметр настройки должен быть либо dict, либо str (путь к файлу настройки).")
        self.connection = None

    def connect(self):
        if not isinstance(self.config, dict): raise ValueError("Настройка должна представлять собой словарь, содержащий параметры подключения к базе данных.")
        try:
            self.connection = mysql.connector.connect(
                host=self.config.get('host', 'localhost'),
                user=self.config.get('user', 'root'),
                password=self.config.get('password', ''),
                database=self.config.get('database', '')
            )
            print(f"Подключено к базе данных: {self.config.get('database')}")
        except mysql.connector.Error as e: raise RuntimeError(f"Ошибка подключения к базе данных: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Отключено от базы данных.")

    def add_user(self, username, password):
        if not self.connection: raise RuntimeError("Нет активного подключения к базе данных.")
        try:
            cursor = self.connection.cursor(dictionary=True)

            cursor.execute("SELECT COUNT(*) AS count FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result['count'] > 0: raise ValueError(f"Логин '{username}' уже существует.")

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            self.connection.commit()
            print(f"Пользователь '{username}' успешно добавлен.")
        except mysql.connector.Error as e: raise RuntimeError(f"Ошибка при добавлении пользователя: {e}")
        finally: cursor.close()

if __name__ == "__main__":
    db = Db('db_config.json')
    db.connect()
    
    try: db.add_user("test_user", "secure_password")
    except ValueError as ve: print(f"Ошибка: {ve}")
    except RuntimeError as re: print(f"Ошибка системы: {re}")
    db.close()