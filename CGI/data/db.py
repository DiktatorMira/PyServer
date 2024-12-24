import json
import mysql
import mysql.connector
import data.db_config

class Db:
    def __init__(self,): self.__connection = None

    def get_connection(self):
        if self.__connection is None: self.__connection = mysql.connector.connect(**data.db_config.mysql_connection_data)
        return self.__connection