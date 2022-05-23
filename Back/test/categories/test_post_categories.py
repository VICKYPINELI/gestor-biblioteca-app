from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category
from src.domain.users import User,UserRepository



# #---------------------------------------AÑADIENDO CATEGORIAS EN POST
def test_should_return_books_with_its_categories():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    users_repository = UserRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository,
                                   "users": users_repository})
    client = app.test_client()
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=1
        )
    )
    categories_repository.save(
        Category(
            category_id="1",
            category="horror"
        ))
    categories_repository.save(
        Category(
            category_id="2",
            category="drama"
        ))
    categories_repository.save(
        Category(
            category_id="3",
            category="comedia"
        ))
    categories_repository.save(
        Category(
            category_id="4",
            category="aventura"
        ))
    book={
        "id": "book-1",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
        "categories":["1","2","3","4"]
    }
    response = client.post("/api/books",headers={'Authorization':'user_1'},json=book)

    response = client.get("/api/books")
    assert response.json == [
        {
            "id": "book-1",
            "title": "test title",
            "author": "test author",
            "publisher": "test publisher",
            "ean": 1111,
            "categories": ["horror","drama","comedia","aventura"]
        },
    ]

# #---------------------------------------AÑADIENDO CATEGORIAS CON LISTA VACIA

def test_should_save_book_if_categories_list_empty():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    users_repository = UserRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository,
                                   "users": users_repository})
    client = app.test_client()
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=1))
    book={
        "id": "book-1",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
        "categories":[]
    }
    response = client.post("/api/books",headers={'Authorization':'user_1'},json=book)

    response = client.get("/api/books")
    assert response.json == [
        {
            "id": "book-1",
            "title": "test title",
            "author": "test author",
            "publisher": "test publisher",
            "ean": 1111,
            "categories": []
        },
    ]