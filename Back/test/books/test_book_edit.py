from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category
from src.domain.users import User,UserRepository


def test_method_should_edit_one_book():
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
    book_data = Book(
        "book-1", "edited title", "edited author", "edited publisher", 2222
    )
    books_repository.edit(book_data)
    response_get = client.get("/api/books/book-1")

    assert response_get.json == {
        "id": "book-1",
        "title": "edited title",
        "author": "edited author",
        "publisher": "edited publisher",
        "ean": 2222,
        "categories": [],
    }


def test_server_should_edit_one_book():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    users_repository = UserRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository,"users": users_repository})
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
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=1
        )
    )
    book_data = {
        "id": "book-1",
        "title": "modified book",
        "author": "modified author",
        "publisher": "edited publisher",
        "ean": 2222,
    }

    response = client.put("/api/books/book-1", json=book_data, headers={'Authorization':'user_1'})
    assert response.status_code == 200

    response_get = client.get("/api/books/book-1")
    assert response_get.json == {
        "id": "book-1",
        "title": "modified book",
        "author": "modified author",
        "publisher": "edited publisher",
        "ean": 2222,
        "categories": [],
    }

#---------------------------------------------------------------------->

def test_server_should_not_allow_to_edit_a_book_if_not_allowed():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    users_repository = UserRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository,"users": users_repository})
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
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=0
        )
    )
    book_data = {
        "id": "book-1",
        "title": "modified book",
        "author": "modified author",
        "publisher": "edited publisher",
        "ean": 2222,
    }

    response = client.put("/api/books/book-1", json=book_data, headers={'Authorization':'user_1'})
    assert response.status_code == 403

#------------------------------------------------------------------------->

def test_server_should_not_allow_to_edit_a_book_if_user_doesnt_exist():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    users_repository = UserRepository(database)
    app = create_app(repositories={"books": books_repository,
                                   "categories": categories_repository,"users": users_repository})
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
    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=0
        )
    )
    book_data = {
        "id": "book-1",
        "title": "modified book",
        "author": "modified author",
        "publisher": "edited publisher",
        "ean": 2222,
    }

    response = client.put("/api/books/book-1", json=book_data, headers={'Authorization':'user_2'})
    assert response.status_code == 403


    

