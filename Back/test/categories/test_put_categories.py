from src.lib.utils import temp_file
from src.webserver import create_app
from src.domain.books import BookRepository, Book
from src.domain.categories import CategoriesRepository, Category
from src.domain.users import User,UserRepository



# #---------------------------------------MODIFICANDO CATEGORIAS EN POST
def test_should_delete_categories_final_purpose_is_modifying_in_bookscategories():
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
    
    #categorias guardadas en tabla bookscategories
    books_repository.add_category("book-1",[2,5])
    result=categories_repository.search_categories_in_books_categories("book-1")
    assert result ==[{'book_id': 'book-1', 'category_id': 2},{'book_id': 'book-1', 'category_id': 5}]

    #new categories to add
    modified_categories={
        "book_id": "book-1",
        "categories": [3]
    }

    #borrar categorias en tabla intermedia p/luego agregar nuevas
    response = client.put("/api/categories",json=modified_categories, headers={'Authorization':'user_1'})
    assert response.status_code == 200

       
    result=categories_repository.search_categories_in_books_categories("book-1")
    assert result==[{'book_id': 'book-1', 'category_id': 3}]
    
#--------------------------------------------------->

def test_modify_categories_if_no_categories_saved_before():
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
    
    result=categories_repository.search_categories_in_books_categories("book-1")
    assert result == []

    #new categories to add
    modified_categories={
        "book_id": "book-1",
        "categories": [3,4]
    }

    response = client.put("/api/categories",json=modified_categories, headers={'Authorization':'user_1'})
    assert response.status_code == 200

       
    result=categories_repository.search_categories_in_books_categories("book-1")
    assert result==[{'book_id': 'book-1', 'category_id': 3},{'book_id': 'book-1', 'category_id': 4}]    
    
    
