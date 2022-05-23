import sys


sys.path.insert(0, "")


def data_organizer():
    from src.domain.users import UserRepository, User
    from src.domain.info import InfoRepository, Info
    from src.domain.loans import LoanRepository, Loan
    from src.domain.books import BookRepository, Book
    from src.domain.categories import CategoriesRepository, Category
    import sqlite3
    database_path = "data/database.db"

    info_repository = InfoRepository(database_path)

    info_repository.save(Info("library-app"))

    book_repository = BookRepository(database_path)

    book_repository.save(
        Book(
            id="book-1",
            title="Mas grandes que el amor",
            author="Dominique Lapiere",
            publisher="Planeta",
            ean=1111,
        )
    )

    book_repository.save(
        Book(
            id="book-2",
            title="El Quijote",
            author="M. de Cervantes",
            publisher="Ruti",
            ean=1656,
        )
    )

    book_repository.save(
        Book(
            id="book-3",
            title="El Libro Negro de las Horas",
            author="Eva García Sáenz de Urturi",
            publisher="Planeta",
            ean=165656,
        )
    )

    book_repository.save(
        Book(
            id="book-4",
            title="El peligro de estar cuerda",
            author="Rosa Montero",
            publisher="Erein",
            ean=165656,
        )
    )

    book_repository.save(
        Book(
            id="book-5",
            title="La Bestia",
            author="Carmen Mola",
            publisher="Akala",
            ean=51556,
        )
    )
    book_repository.save(
        Book(
            id="book-6",
            title="Carrie",
            author="Stephen King",
            publisher="Akala",
            ean=51556,
        )
    )

    user_repository = UserRepository(database_path)

    user_lib = User('user_1', 'Bibliotecaria', True)

    user1 = User('user_2', 'Usuario', False)
    user2 = User('user_3', 'Usuaria', False)

    user_repository.save(user_lib)
    user_repository.save(user1)
    user_repository.save(user2)

    loan_repository = LoanRepository(database_path)

    loan1 = Loan("1", "book-1", "user_1","2022-04-10","")
    loan2 = Loan("2", "book-2", "user_2", "2022-04-08", "")

    loan_repository.save(loan1)
    loan_repository.save(loan2)

    categories_repository = CategoriesRepository(database_path)
    category_1 = Category("1", "horror")
    category_2 = Category("2", "drama")
    category_3 = Category("3", "comedia")
    category_4 = Category("4", "aventura")
    category_5 = Category("5", "aprendizaje")

    categories_repository.save(category_1)
    categories_repository.save(category_2)
    categories_repository.save(category_3)
    categories_repository.save(category_4)
    categories_repository.save(category_5)

    con = sqlite3.connect(database_path)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("""INSERT INTO bookscategories(book_id, category_id)
                    VALUES
                        ("book-1","1"),
                        ("book-2","2"),
                        ("book-3","3"),
                        ("book-4","4"),
                        ("book-4","2"),
                        ("book-4","3"),
                        ("book-5","1"),
                        ("book-5","5")""")
    con.commit()
    cur.close()


# con = sqlite3.connect(database_path)
#     con.row_factory = sqlite3.Row

#     cur = con.cursor()

#     cur.execute(
#         """CREATE TABLE books
#     ("id" TEXT,
#     "title" TEXT,
#     "author" TEXT,
#     "publisher" TEXT,
#     "ean" INTEGER, PRIMARY KEY("id"))"""
#     )

#     cur.execute(
#         """INSERT INTO books
#     VALUES
#     ('book-1', 'Escenografía y maquillaje',
#      'Martí, Mònica', 'Parramon', '978843342202'),
#     ('book-2', 'Titeres y mimo', 'Martí, Mònica', 'Parramon',    '978843342208'),
#     ('book-3', 'Carrie',    'King, Stephen',    'Debolsillo',    '978843342206'),
#     ('book-4', 'Armas, gérmenes y acero',
#      'Diamond, Jared',    'Debolsillo',    '978843342204'),
#     ('book-5', 'Egipto',    'Bargallo, Eva',    'Parramon',    '978843342200'); """
#     )

#     cur.execute(
#         """CREATE TABLE users
#     ("user_id" TEXT,
#     "user" TEXT,
#     "is_librarian" INTGER,
#     PRIMARY KEY("user_id"))"""
#     )

#     cur.execute(
#         """INSERT INTO users
#     VALUES
#     ('user_1', 'Paco Fernandez', True),
#     ('user_2', 'Bob Deeb', False),
#     ('user_3', 'Anna', False); """
#     )
#     cur.execute(
#         """
#                 CREATE TABLE if not exists loans(
#                     "loan_id" TEXT,
#                     "book_id" TEXT,
#                     "user_id" TEXT,
#                     PRIMARY KEY("loan_id")
#                 )
#             """
#     )

#     con.commit()
#     cur.close()

data_organizer()
