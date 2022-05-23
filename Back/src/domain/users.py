import sqlite3


class User:
    def __init__(self, user_id, user, is_librarian):
        self.user_id = user_id
        self.user = user
        self.is_librarian = is_librarian

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user": self.user,
            "is_librarian": self.is_librarian,

        }


class UserRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            CREATE TABLE if not exists users(
                "user_id" TEXT,
                "user" TEXT,
                "is_librarian" INTEGER, 
                PRIMARY KEY("user_id") 
            )
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def get_users(self):
        sql = """select * from users"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchall()

        result = []
        for item in data:
            user = User(**item)
            result.append(user)

        return result

    def save(self, user):
        sql = """insert into users (user_id, user, is_librarian) values (
           :user_id, :user,:is_librarian 
        ) """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, user.to_dict())
        conn.commit()

    def get_user_by_id(self, id):
        sql = """SELECT * FROM users WHERE user_id = :id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": id})
        data = cursor.fetchone()
        if data!=None:
            selected_user = User(**data)
            return selected_user
        else:
            return None
