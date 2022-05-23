from src.lib.utils import temp_file

from src.domain.loans import LoanRepository, Loan


def test_should_return_loan():
    loans_repository = LoanRepository(temp_file())

    test_loan = Loan(loan_id="loan_1", book_id="book_1", user_id="user_1",
                        initial_date="2020-04-10",final_date="2020-04-20")
    loans_repository.save(test_loan)

    get_loan = loans_repository.get_loan_by_id("loan_1")

    assert get_loan.to_dict() == test_loan.to_dict()
