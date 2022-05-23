import sqlite3


class Category:
    def __init__(self, category_id, category):
        self.category_id = category_id
        self.category = category

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category": self.category,
        }


class CategoriesRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql1 = """
            CREATE TABLE if not exists categories(
                "category_id" VARCHAR PRIMARY KEY, 
                "category" VARCHAR
            )
        """
        sql2 = """
            CREATE TABLE if not exists bookscategories (
            "book_id"    TEXT,
            "category_id"    INTEGER,
            FOREIGN KEY("category_id") REFERENCES "categories"("category_id"),
            FOREIGN KEY("book_id") REFERENCES "books"("id") ON DELETE CASCADE
            )
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
        conn.commit()

    def get_categories(self):
        sql = """select * from categories"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchall()
        result = []
        for item in data:
            category = Category(**item)
            result.append(category)

        return result

    def save(self, category):
        sql = """INSERT INTO categories(category_id, category) values
        (:category_id, :category
        )"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, category.to_dict())
        conn.commit()
    
    def search_categories_in_books_categories(self,id_book):
        sql = """select * from bookscategories
                where book_id=?"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql,(id_book,))
        data = cursor.fetchall()
        categories_list=[dict(row) for row in data]
        return categories_list

    def delete_categories(self,id_book):
        sql = """DELETE from bookscategories
                where book_id= :book_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql,{"book_id": id_book})
        conn.commit()
        