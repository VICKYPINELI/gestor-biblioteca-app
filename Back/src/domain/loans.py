import sqlite3
from datetime import datetime 


class Loan:
    def __init__(self, loan_id, book_id, user_id,initial_date=None, final_date=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.user_id = user_id
        self.final_date=final_date
        self.initial_date = initial_date

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "initial_date":self.initial_date,
            "final_date":self.final_date
        }


class LoanRepository:
    def __init__(self, database_path):
        self.database_path = database_path
        self.init_tables()

    def create_conn(self):
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        sql = """
            CREATE TABLE if not exists loans (
                "loan_id" TEXT,
                "book_id" TEXT,
                "user_id" TEXT , 
                "initial_date" TEXT,
                "final_date" TEXT,
                PRIMARY KEY("loan_id")
            )
        """

        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def get_loans_users(self, user_id):
        sql = """SELECT books.title, loans.loan_id, loans.book_id, loans.initial_date, loans.final_date
                    FROM loans
                INNER JOIN books ON loans.book_id = books.id
                WHERE loans.user_id = ? """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))

        data = cursor.fetchall()

        result = []
        for item in data:
            loan = {
                "loan_id": item["loan_id"],
                "book_id": item["book_id"],
                "title": item["title"],
                "initial_date":item["initial_date"],
                "final_date":item["final_date"]
            }
            result.append(loan)
        return result

    def get_loans_librarian(self):
        sql = """SELECT books.title, loans.loan_id, loans.book_id, users.user_id, users.user, loans.initial_date, loans.final_date
              FROM loans 
              INNER JOIN users
              INNER JOIN books 
              ON loans.book_id = books.id AND loans.user_id = users.user_id AND loans.final_date IS NULL
             """

        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql)

        data = cursor.fetchall()

        result = []
        for item in data:
            loan = {
                "loan_id": item["loan_id"],
                "book_id": item["book_id"],
                "title": item["title"],
                "user_id": item["user_id"],
                "user": item["user"],
                "initial_date":item["initial_date"],
                "final_date":item["final_date"]
            }
            result.append(loan)

        return result

    def get_loan_by_id(self, loan_id):
        sql = """SELECT * FROM loans
        WHERE loans.loan_id == :id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"id": loan_id})

        data = cursor.fetchone()
        this_loan = Loan(**data)
        return this_loan

    def save(self, loan):
        sql = """insert into loans (loan_id, book_id, user_id, initial_date, final_date) values (
           :loan_id, :book_id, :user_id, :initial_date, :final_date
        ) """
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, loan.to_dict())
        conn.commit()

    def delete(self, loan_id):
        sql = """DELETE FROM loans WHERE loan_id = :loan_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"loan_id": loan_id})

        conn.commit()

    def is_loaned(self, book_id):
        sql = """SELECT * FROM loans
        WHERE loans.book_id == :book_id"""
        conn = self.create_conn()
        cursor = conn.cursor()
        cursor.execute(sql, {"book_id": book_id})

        data = cursor.fetchall()
        if data == []:
            return False
        else:
            return True
    
    def loan_edit(self, loan):
        sql = """UPDATE loans SET final_date= ? WHERE loan_id = ?"""
        conn = self.create_conn()
        cursor = conn.cursor()
        if (loan.final_date!=''):
            cursor.execute(
            sql, (loan.final_date, loan.loan_id)
            )
        else:
            today_to_parse=datetime.now().isoformat()
            today=today_to_parse[0:10]
            cursor.execute(
            sql, (today, loan.loan_id)
            )
        conn.commit()
