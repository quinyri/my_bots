import sqlite3
from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def execute_script(self, script, parameters=()):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLiteDatabase(DatabaseInterface):
    def __init__(self, name: str):
        self.name = name
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.name)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_script(self, script, parameters=()):
        try:
            with self.connect() as connection:
                cursor = connection.cursor()
                if parameters:
                    cursor.execute(script, parameters)
                else:
                    cursor.executescript(script)
                connection.commit()
                return cursor
        except Exception as e:
            print(f"An error occurred: {str(e)}")


class UserRepository:
    def __init__(self, db: DatabaseInterface):
        self.db = db

    def input_user_id(self, user_id: int):
        with open('sqls/input_user_id.sql', 'r') as fh:
            script = fh.read()
            self.db.execute_script(script, (user_id,))

    def input_fav_urls(self, user_id: int, url: str):
        with open('sqls/input_fav_urls.sql', 'r') as fh:
            script = fh.read()
            self.db.execute_script(script, (user_id, url))

    def input_all_urls(self, user_id: int, urls: list):
        with open('sqls/input_all_urls.sql', 'r') as fh:
            script = fh.read()
            for url in urls:
                print(url)
                self.db.execute_script(script, (user_id, url))

    def get_fav_url(self, user_id: int):
        with open('sqls/get_fav_urls.sql', 'r') as fh:
            script = fh.read()
            return self.db.execute_script(script, (user_id,)).fetchone()

    def get_one_url(self, user_id: int):
        with open('sqls/get_all_urls.sql', 'r') as fh:
            script = fh.read()
            return self.db.execute_script(script, (user_id,)).fetchone()

    def get_all_urls(self, user_id: int):
        with open('sqls/get_all_urls.sql', 'r') as fh:
            script = fh.read()
            return self.db.execute_script(script, (user_id,)).fetchall()

    def delete_fav_url(self, user_id: int, url: str):
        with open('sqls/delete_fav_urls.sql', 'r') as fh:
            script = fh.read()
            self.db.execute_script(script, (user_id, url))

    def delete_one_url(self, user_id: int, url: str):
        with open('sqls/delete_all_urls.sql', 'r') as fh:
            script = fh.read()
            self.db.execute_script(script, (user_id, url))

