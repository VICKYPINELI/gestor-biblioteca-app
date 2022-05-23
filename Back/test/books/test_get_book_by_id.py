from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category


def test_should_return_one_book_by_id():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository})
    client = app.test_client()

    books_repository.save(
        Book(
            id="book-1",
            title="test title",
            author="test author",
            publisher="test publisher",
            ean=1111,
        )
    )
    categories_repository.save(
        Category(
            category_id="1",
            category="horror"
        )
    )
    books_repository.add_category(
        book_id="book-1",
        categories="1"

    )

    response = client.get("/api/books/book-1")
    assert response.json == {
        "id": "book-1",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
        "categories": ["horror"]
    }

#------------------------------------------------------------>

def test_should_return_error_if_book_doesnt_exist():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository})
    client = app.test_client()

    response = client.get("/api/books/book-2")
    assert response.status_code == 404