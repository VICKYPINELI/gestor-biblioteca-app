from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category
from src.domain.users import User,UserRepository


def test_server_should_save_one_book():
    database = temp_file()
    books_repository = BookRepository(database)
    users_repository = UserRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "users": users_repository,
                                   "categories": categories_repository})
    client = app.test_client()
    book={
        "id": "book-1",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
        "categories":["1","2","3","4"]
    }
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=1
        )
    )
    

    response = client.post("/api/books",headers={'Authorization':'user_1'},json=book)
    assert response.status_code==200

#---------------------------------------------------------->

def test_server_should_not_allow_to_add_a_book_if_doesnt_exist():
    database = temp_file()
    books_repository = BookRepository(database)
    users_repository = UserRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "users": users_repository})
    client = app.test_client()
    book={
        "id": "book-1",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
    }
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=1
        )
    )
    

    response = client.post("/api/books",headers={'Authorization':'user_2'},json=book)
    assert response.status_code==403