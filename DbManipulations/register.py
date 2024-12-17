import cgi
import cgitb
from db import Db

cgitb.enable()
print("Content-Type: text/html; charset=utf-8\n")

form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")

if not username or not password: print("<h2>Ошибка: Имя пользователя и пароль обязательны!</h2>")
else: db = Db('db_config.json')
    try:
        db.connect()
        db.add_user(username, password)
        print(f"<h2>Пользователь '{username}' успешно зарегистрирован!</h2>")
    except ValueError as ve: print(f"<h2>Ошибка: {ve}</h2>")
    except RuntimeError as re: print(f"<h2>Ошибка системы: {re}</h2>")
    finally: db.close()