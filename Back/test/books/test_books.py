from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category
from src.domain.users import User,UserRepository

def test_should_return_books_in_database():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(
        repositories={"books": books_repository, "categories": categories_repository})
    client = app.test_client()

    books_repository.save(
        Book(
            id="id",
            title="test title",
            author="test author",
            publisher="test publisher",
            ean=1111
        )
    )
    
    categories_repository.save(
        Category(
            category_id="1",
            category="horror"
        )
    )
    books_repository.add_category("id", "1")

    response = client.get("/api/books")
    assert response.json == [
        {
            "id": "id",
            "title": "test title",
            "author": "test author",
            "publisher": "test publisher",
            "ean": 1111,
            "categories": ["horror"]
        },
    ]

