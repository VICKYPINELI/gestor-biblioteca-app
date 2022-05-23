import sqlite3
from unicodedata import category


class Book:
    def __init__(self, id, title, author, publisher, ean):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.ean = ean
        self.categories = []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "ean": self.ean,
            "categories": self.categories,
        }


class BookRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            CREATE TABLE if not exists books (
                "id" TEXT,
                "title" TEXT,
                "author" TEXT,
                "publisher" TEXT,
                "ean" INTEGER, PRIMARY KEY("id")
            )
        """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def get_books(self):
        sql = """select * from books"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchall()

        result = []
        for item in data:
            book = Book(**item)
            book_categories = self.get_book_categories(book)
            book.categories = book_categories
            result.append(book)

        return result

    def get_book_by_id(self, id):
        sql = """SELECT * FROM books WHERE id = :id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": id})
        data = cursor.fetchone()
        # print('******data',data)
        if data!=None:
            book = Book(**data)
            book_categories = self.get_book_categories(book)
            book.categories = book_categories
            return book
        return None

    def get_book_categories(self, book):
        book_id = book.id
        sql = """SELECT categories.category
                FROM bookscategories
                INNER JOIN categories USING (category_id)
                WHERE book_id = :book_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"book_id": book_id})

        data = cursor.fetchall()
        categories_list = []
        for item in data:
            book_category = item["category"]
            categories_list.append(book_category)
        return categories_list

    def delete(self, id):
        sql = """DELETE FROM books WHERE id = :id"""
        conn = self.create_conn()
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute(sql, {"id": id})

        conn.commit()

    def save(self, book):
        sql = """INSERT INTO books (id, title, author, publisher, ean) values (
           :id, :title, :author, :publisher,:ean
        ) """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(
            sql,
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "ean": book.ean,
            },
        )
        conn.commit()

    def edit(self, book):
        sql = """UPDATE books SET title= ?, author = ?, publisher= ?, ean= ? WHERE id = ?"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(
            sql, (book.title, book.author, book.publisher, book.ean, book.id)
        )
        conn.commit()

    def add_category(self, book_id, categories):
        sql = """ INSERT INTO bookscategories (book_id, category_id)
                            VALUES (:book_id, :category_id)
                    """
        conn = self.create_conn()
        cursor = conn.cursor()
        for category in categories:
            cursor.execute(sql, {"book_id": book_id, "category_id": category})
            conn.commit()
