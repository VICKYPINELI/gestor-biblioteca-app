
from src.lib.utils import temp_file, object_to_json

from src.webserver import create_app
from src.domain.loans import LoanRepository, Loan
from src.domain.users import UserRepository, User
from src.domain.books import BookRepository, Book

def test_delete_method_should_delete_loaned_book_happy_path():
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
            final_date=""
        )
    )

    loans_repository.save(
        Loan(
            loan_id="loan-2",
            book_id="titeres2",
            user_id="user_2",
            initial_date="2020-04-10",
            final_date=""
        )
    )

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=False
        )
    )

    response_before = client.get("/api/loans", headers={'Authorization': 'user_1'})

    response_delete = client.delete("/api/loans/loan-1", headers={'Authorization': 'user_1'})

    response_after = client.get("/api/loans", headers={'Authorization': 'user_1'})

    assert response_before.json == [
        {
            "loan_id": "loan-1",
            "book_id": "titeres",
            "title": "test title",
            "initial_date":"2020-04-10",
            "final_date":""
        }
    ]

    assert response_delete.status_code == 200

    assert response_after.json == []

def test_delete_method_without_authorization_should_return_403():
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
            final_date=""
        )
    )

    loans_repository.save(
        Loan(
            loan_id="loan-2",
            book_id="titeres2",
            user_id="user_2",
            initial_date="2020-04-10",
            final_date=""
        )
    )

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=False
        )
    )

    response_before = client.get("/api/loans", headers={'Authorization': 'user_1'})

    response_delete = client.delete("/api/loans/loan-1", headers={'Authorization': 'user_2'})

    response_after = client.get("/api/loans", headers={'Authorization': 'user_1'})

    assert response_before.json == [
        {
            "loan_id": "loan-1",
            "book_id": "titeres",
            "title": "test title",
            "initial_date":"2020-04-10",
            "final_date":""
        }
    ]

    assert response_delete.status_code == 403

    assert response_after.json == [
        {
            "loan_id": "loan-1",
            "book_id": "titeres",
            "title": "test title",
            "initial_date":"2020-04-10",
            "final_date":""
        }
    ]