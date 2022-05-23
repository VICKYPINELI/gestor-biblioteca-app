from src.domain.loans import LoanRepository
from src.domain.books import BookRepository
from src.webserver import create_app
from src.domain.info import InfoRepository
from src.domain.users import UserRepository
from src.domain.categories import CategoriesRepository


database_path = "data/database.db"

repositories = {
    "info": InfoRepository(database_path),
    "books": BookRepository(database_path),
    "users": UserRepository(database_path),
    "loans": LoanRepository(database_path),
    "categories": CategoriesRepository(database_path),
}

app = create_app(repositories)

app.run(debug=True, host="0.0.0.0", port="5000")
