
from src.lib.utils import temp_file, object_to_json

from src.webserver import create_app
from src.domain.loans import LoanRepository, Loan
from src.domain.users import UserRepository, User
from src.domain.books import BookRepository, Book


def test_should_get_loans_for_users():
    database = temp_file()
    loans_repository = LoanRepository(database)
    users_repository = UserRepository(database)
    books_repository = BookRepository(database)
    app = create_app(
        repositories={"loans": loans_repository, "users": users_repository, "books": books_repository})
    client = app.test_client()

    books_repository.save(
        Book(
            id="titeres",
            title="test title",
            author="test author",
            publisher="test publisher",
            ean=1111,
        )
    )
    books_repository.save(
        Book(
            id="titeres2",
            title="test title",
            author="test author",
            publisher="test publisher",
            ean=1111,
        )
    )

    loans_repository.save(
        Loan(
            loan_id="loan-1",
            book_id="titeres",
            user_id="user_1",
            initial_date="2020-04-10",
            final_date="2020-04-20"
        )
    )

    loans_repository.save(
        Loan(
            loan_id="loan-2",
            book_id="titeres2",
            user_id="user_2",
            initial_date="2020-04-10",
            final_date="2020-04-20"
        )
    )

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=False
        )
    )

    response = client.get("/api/loans", headers={'Authorization': 'user_1'})

    assert response.json == [
        {
            "loan_id": "loan-1",
            "book_id": "titeres",
            "title": "test title",
            "initial_date":"2020-04-10",
            "final_date":"2020-04-20"
        }
    ]


def test_should_get_loans_for_librarian():
    database = temp_file()
    loans_repository = LoanRepository(database)
    users_repository = UserRepository(database)
    books_repository = BookRepository(database)
    app = create_app(
        repositories={"loans": loans_repository, "users": users_repository, "books": books_repository})
    client = app.test_client()

    books_repository.save(
        Book(
            id="titeres",
            title="test title1",
            author="test author",
            publisher="test publisher",
            ean=1111,
        )
    )
    books_repository.save(
        Book(
            id="titeres2",
            title="test title2",
            author="test author",
            publisher="test publisher",
            ean=1111,
        )
    )

    loans_repository.save(
        Loan(
            loan_id="loan-1",
            book_id="titeres",
            user_id="user_1",
            initial_date="2020-04-07",
            final_date="2020-04-27"
        )
    )

    loans_repository.save(
        Loan(
            loan_id="loan-2",
            book_id="titeres2",
            user_id="user_2",
            initial_date="2020-04-08"
            #no me llega final_date cuando reservó, esto se genera al devolver
        )
    )

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario1",
            is_librarian=True
        )
    )
    users_repository.save(
        User(
            user_id="user_2",
            user="usuario2",
            is_librarian=False
        )
    )

    response = client.get("/api/loans", headers={'Authorization': 'user_1'})

    assert response.json == [
        {
            "loan_id": "loan-2",
            "book_id": "titeres2",
            "user_id": "user_2",
            "title": "test title2",
            "user": "usuario2",
            "initial_date":"2020-04-08",
            "final_date":None
        }
    ]
