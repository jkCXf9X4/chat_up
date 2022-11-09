import sqlite3
import time
import os


class Message:
    columns = ["user", "nick", "time", "message"]
    columns_coma = f"{', '.join(columns)}"
    columns_coma_parenthesis = f"({columns_coma})"

    def __init__(self, user, nick, time, message) -> None:
        self.user = user
        self.nick = nick
        self.time = time
        self.message = message

    def __str__(self) -> str:
        return f"('{self.user}', '{self.nick}', {self.time}, '{self.message}')"


class DBwrapper:
    def __init__(self, name, dir: str) -> None:
        self.dbname = name + ".db"
        self.path = os.path.join(dir, self.dbname)
        print(self.path)
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

        self.tablename = "chat"
        self.columns = Message.columns

    def try_create_table(self):
        table_query = f"CREATE TABLE IF NOT EXISTS {self.tablename} {Message.columns_coma_parenthesis}"
        # print(table_query)
        self.cursor.execute(table_query)

        table_query = f"CREATE TABLE IF NOT EXISTS online (user NOT NULL PRIMARY KEY, time)"
        self.cursor.execute(table_query)

    def close(self):
        self.cursor.close()
        self.connection.close()

    def add_message(self, user, nick, message):
        m = Message(user=user, nick=nick, time=time.time(), message=message)
        s = f"INSERT INTO {self.tablename} VALUES {m}"
        # print(s)
        self.cursor.execute(s)
        self.connection.commit()

    def get_new_messages(self, last_fetch):
        result = self.cursor.execute(
            f"SELECT {Message.columns_coma} FROM {self.tablename} WHERE time > {last_fetch}")
        messages = [Message(*i) for i in result.fetchall()]
        # print(f"{len(messages)} new messages")
        return messages

    def set_user_online(self, user):
        s = f"INSERT OR REPLACE INTO online VALUES ('{user}', '{time.time()}')"
        self.cursor.execute(s)
        self.connection.commit()

    def get_users(self):
        now = time.time()
        one_minutes_back = now - 60.0
        result = self.cursor.execute(f"SELECT * FROM online")
        users = []
        for i in result.fetchall():
            if float(i[1]) > one_minutes_back:
                users.append(i[0])
        return users


class ChatHandler:

    def __init__(self, user, nick, file_name, directory: str):
        self.user = user
        self.nick = nick
        self.directory = directory
        self.db = DBwrapper(file_name, self.directory)

        self.db.try_create_table()
        self.latest_fetch_time = 0.0

    def add_message(self, message):
        self.db.add_message(self.user, self.nick, message)

    def get_new_messages(self):
        m = self.db.get_new_messages(self.latest_fetch_time)
        self.latest_fetch_time = time.time()
        return m

    def set_user_online(self):
        self.db.set_user_online(self.user)

    def get_online_users(self):
        return self.db.get_users()

    def close(self):
        self.db.close()
