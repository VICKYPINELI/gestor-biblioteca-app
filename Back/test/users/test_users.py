from src.lib.utils import temp_file

from src.webserver import create_app
from src.domain.users import UserRepository, User


def test_should_return_books_in_database():
    users_repository = UserRepository(temp_file())
    app = create_app(repositories={"users": users_repository})
    client = app.test_client()

    users_repository.save(
        User(
            user_id="user_1",
            user="usuario",
            is_librarian=True
        )
    )

    response = client.get("/api/users")
    assert response.json == [
        {
            "user_id": "user_1",
            "user": "usuario",
            "is_librarian": True
        },
    ]
