import mysql.connector
import json

class Db:
    def __init__(self, config):
        if isinstance(config, dict):
            if 'db' in config: self.config = config['db']
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

if __name__ == "__main__":
    db = Db('db_config.json')
    db.connect()
    db.close()