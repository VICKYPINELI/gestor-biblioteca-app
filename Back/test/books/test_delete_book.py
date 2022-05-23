from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category
from src.domain.users import User,UserRepository


#test del server delete
def test_server_should_delete_one_book():
    database = temp_file()
    books_repository = BookRepository(database)
    users_repository = UserRepository(database)
    app = create_app(
        repositories={"books": books_repository, "users": users_repository}
    )
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
    response = client.delete("/api/books/book-1",headers={'Authorization':'user_1'})
    assert response.status_code==200

#-------------------------------------------------------------->

def test_server_should_not_permit_to_delete_a_book_if_user_doesnt_exist():
    database = temp_file()
    books_repository = BookRepository(database)
    users_repository = UserRepository(database)
    app = create_app(
        repositories={"books": books_repository, "users": users_repository}
    )
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
    response = client.delete("/api/books/book-1",headers={'Authorization':'user_2'})
    assert response.status_code==403

###test del método delete

def test_delete_method_should_delete_one_book():
    database = temp_file()
    books_repository = BookRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(
        repositories={"books": books_repository, "categories": categories_repository}
    )
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
    books_repository.save(
        Book(
            id="book-2",
            title="test title",
            author="test author",
            publisher="test publisher",
            ean=2222,
        )
    )
    books_repository.delete("book-1")

    response_get = client.get("/api/books")
    assert response_get.json == [
        {
            "id": "book-2",
            "title": "test title",
            "author": "test author",
            "publisher": "test publisher",
            "ean": 2222,
            "categories": [],
        }
    ]

#-----------------------------------------------------------------

def test_server_should_delete_one_book_with_categories():
    database = temp_file()
    books_repository = BookRepository(database)
    users_repository = UserRepository(database)
    categories_repository = CategoriesRepository(database)
    app = create_app(
        repositories={"books": books_repository, "users": users_repository,
        "categories": categories_repository}
    )
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
    book1={
        "id": "book-1",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
        "categories":["1","2"]
    }
    book2={
        "id": "book-2",
        "title": "test title",
        "author": "test author",
        "publisher": "test publisher",
        "ean": 1111,
        "categories":["1","2"]
    }
    response =client.post("/api/books",headers={'Authorization':'user_1'},json=book1)
    response =client.post("/api/books",headers={'Authorization':'user_1'},json=book2)
    response = client.delete("/api/books/book-1",headers={'Authorization':'user_1'})
    response = client.get("/api/books")
    assert response.json == [{
            "id": "book-2",
            "title": "test title",
            "author": "test author",
            "publisher": "test publisher",
            "ean": 1111,
            "categories":["horror","drama"]
    }]
    check_categories_yet_exist=categories_repository.search_categories_in_books_categories("book-1")
    assert check_categories_yet_exist==[]

    



