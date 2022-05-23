from src.lib.utils import temp_file, object_to_json
from src.webserver import create_app
from src.domain.loans import LoanRepository, Loan
from src.domain.users import UserRepository, User
from src.domain.books import BookRepository, Book


def test_should_add_return_date_in_loans_if_book_returned():
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

    loans_repository.save(
        Loan(
            loan_id="loan-1",
            book_id="titeres",
            user_id="user_1",
            initial_date="2022-04-10",
            final_date=""
        )
    )

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=True
        )
    )

    body = {"loan_id": "loan-1", "book_id": "book-1", "user_id": "user_1",
            "initial_date": "2022-04-10", "final_date": "2022-04-25"}

    response_before = client.put(
        "/api/loans/loan-1", headers={'Authorization': 'user_1'}, json=body)

    #response_delete = client.delete("/api/loans/loan-2", headers={'Authorization': 'user_1'})

    response_before.status_code == 200

    get_loan = loans_repository.get_loan_by_id("loan-1")

    assert get_loan.final_date == "2022-04-25"
    assert get_loan.to_dict() == {
        "loan_id": "loan-1",
        "book_id": "titeres",
        "user_id": "user_1",
        "initial_date": "2022-04-10",
        "final_date": "2022-04-25"
    }


def test_should_add_return_date_of_today_if_no_date_attribute_comes_from_front():
    from datetime import datetime
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

    loans_repository.save(
        Loan(
            loan_id="loan-1",
            book_id="titeres",
            user_id="user_1",
            initial_date="2022-04-10",
            final_date=""
        )
    )

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=True
        )
    )

    body = {"loan_id": "loan-1", "book_id": "book-1",
            "user_id": "user_1", "initial_date": "2022-04-10", "final_date": ""}
    response_before = client.put(
        "/api/loans/loan-1", headers={'Authorization': 'user_1'}, json=body)
    response_before.status_code == 200

    get_loan = loans_repository.get_loan_by_id("loan-1")

    today_to_parse = datetime.now().isoformat()
    today = today_to_parse[0:10]

    assert get_loan.final_date == today


def test_should_user_not_librarian_can_not_return_a_book():
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

    loans_repository.save(
        Loan(
            loan_id="loan-1",
            book_id="titeres",
            user_id="user_1",
            initial_date="2022-04-10",
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

    body = {"loan_id": "loan-1", "book_id": "book-1", "user_id": "user_1",
            "initial_date": "2022-04-10", "final_date": "2022-04-11"}
    response_before = client.put(
        "/api/loans/loan-1", headers={'Authorization': 'user_1'}, json=body)
    response_before.status_code == 403

    get_loan = loans_repository.get_loan_by_id("loan-1")

    assert get_loan.to_dict() == {
        "loan_id": "loan-1",
        "book_id": "titeres",
        "user_id": "user_1",
        "initial_date": "2022-04-10",
        "final_date": ""
    }
