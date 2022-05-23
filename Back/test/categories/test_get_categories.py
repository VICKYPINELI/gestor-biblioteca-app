from src.domain.books import BookRepository
from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.categories import CategoriesRepository, Category


def test_should_return_categories():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(
        repositories={"categories": categories_repository, "books": books_repository})
    client = app.test_client()

    categories_repository.save(
        Category(
            category_id=1,
            category="category-1"
        )
    )

    response = client.get("/api/categories")
    assert response.json == [
        {
            "category_id": "1",
            "category": "category-1"

        }
    ]
