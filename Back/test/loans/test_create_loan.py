from src.lib.utils import temp_file, object_to_json

from src.webserver import create_app
from src.domain.loans import LoanRepository, Loan
from src.domain.users import UserRepository, User
from src.domain.books import BookRepository, Book
from datetime import date,datetime


def test_loan_should_be_saved():
    database = temp_file()
    loans_repository = LoanRepository(database)
    users_repository = UserRepository(database)
    books_repository = BookRepository(database)
    app = create_app(
        repositories={
            "loans": loans_repository,
            "users": users_repository,
            "books": books_repository,
        }
    )
    client = app.test_client()

    body = {"loan_id": "loan-1", "book_id": "book-1", "user_id": "user_1", "initial_date":"2022-04-10", "final_date":"2022-04-20"}

    response = client.post("/api/loans", json=body)

    assert response.status_code == 200

    saved_loan = loans_repository.get_loan_by_id("loan-1")

    assert saved_loan.to_dict() == {
        "loan_id": "loan-1",
        "book_id": "book-1",
        "user_id": "user_1",
        "initial_date":"2022-04-10",
        "final_date":"2022-04-20"
    }

# def test_should_save_a_loan_if_no_date_puttings_instead_current_day():
#     today=datetime.utcnow().isoformat()
#     today=today[:10]
    
#     database = temp_file()
#     loans_repository = LoanRepository(database)
#     users_repository = UserRepository(database)
#     books_repository = BookRepository(database)
#     app = create_app(
#         repositories={
#             "loans": loans_repository,
#             "users": users_repository,
#             "books": books_repository,
#         }
#     )
#     client = app.test_client()

#     body = {"loan_id": "loan-1", "book_id": "book-1", "user_id": "user_1", "initial_date":"", "final_date":""}

#     response = client.post("/api/loans", json=body)

#     assert response.status_code == 200
#     saved_loan = loans_repository.get_loan_by_id("loan-1")

#     assert saved_loan.to_dict() == {
#         "loan_id": "loan-1",
#         "book_id": "book-1",
#         "user_id": "user_1",
#         "initial_date":today,
#         "final_date":""
#     }


