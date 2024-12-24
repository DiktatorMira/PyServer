from data.db import Db
import data.user_dao

class DbContext:
    def __init__(self):
        self.db = Db()
        self.user_dao = data.user_dao.UserDao(self.db)

    def test_connection(self):
        return self.db.get_connection() is not None
