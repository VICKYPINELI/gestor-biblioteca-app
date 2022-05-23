from flask import Flask, request, jsonify
from flask_cors import CORS
from src.lib.utils import object_to_json
from src.domain.books import Book
from src.domain.loans import Loan
from src.domain.users import User, UserRepository


def create_app(repositories):
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def hello_world():
        return "...magic!"

    @app.route("/api/info", methods=["GET"])
    def info_get():
        info = repositories["info"].get_info()
        return object_to_json(info)

    @app.route("/api/books", methods=["GET"])
    def books_get():
        all_books = repositories["books"].get_books()

        return object_to_json(all_books)

    @app.route("/api/books", methods=["POST"])  # OK
    def add_book():
        user_id = request.headers.get("Authorization")
        user = repositories["users"].get_user_by_id(user_id)
        if(user == None):
            return "", 403
        if user.is_librarian == 1:
            body = request.json
            cat_to_extract = body.pop("categories")
            book_id = body["id"]
            book = Book(**body)
            repositories["books"].save(book)
            repositories["books"].add_category(book_id, cat_to_extract)
            return "", 200
        else:
            return "", 403

    @app.route("/api/books/<id>", methods=["GET"])
    def book_get_by_id(id):
        book = repositories["books"].get_book_by_id(id)
        if book != None:
            return object_to_json(book)
        else:
            return "", 404

    @app.route("/api/books/<id>", methods=["DELETE"])  # OK
    def book_delete_by_id(id):
        user_id = request.headers.get("Authorization")
        user = repositories["users"].get_user_by_id(user_id)
        if(user == None):
            return "", 403
        elif user.is_librarian == 1:
            repositories["books"].delete(id)
            return "", 200
        else:
            return "", 403

    @app.route("/api/books/<id>", methods=["PUT"])  # OK
    def book_edit_by_id(id):
        user_id = request.headers.get("Authorization")
        user = repositories["users"].get_user_by_id(user_id)
        if(user == None):
            return "", 403
        elif user.is_librarian == 1:
            body = request.json
            book = Book(**body)
            repositories["books"].edit(book)
            return "", 200
        else:
            return "", 403

    @app.route("/api/users", methods=["GET"])
    def get_users():
        all_users = repositories["users"].get_users()
        return object_to_json(all_users)

    @app.route("/api/loans", methods=["GET"])
    def get_book_loans():
        user_id = request.headers.get("Authorization")
        user = repositories["users"].get_user_by_id(user_id)

        if user.is_librarian == 1:

            librarian_loans = repositories["loans"].get_loans_librarian()
            return jsonify(librarian_loans), 200

        else:
            user_loans = repositories["loans"].get_loans_users(user_id)
            return jsonify(user_loans), 200

    @app.route("/api/loans", methods=["POST"])
    def reserve_a_book():
        body = request.json
        loan = Loan(**body)
        repositories["loans"].save(loan)
        return ""

    @app.route("/api/loans/<id>", methods=["GET"])
    def book_is_loaned(id):
        loan_book = repositories["loans"].is_loaned(id)
        if loan_book:
            return "true", 200
        else:
            return "false", 404

    @app.route("/api/loans/<id>", methods=["DELETE"])
    def loaned_book_deleted_by_loan_id(id):
        user_id = request.headers.get("Authorization")
        loan = repositories["loans"].get_loan_by_id(str(id))

        is_my_loan = user_id == loan.user_id
        print(user_id)
        print(loan.user_id)
        if is_my_loan:
            repositories["loans"].delete(id)
            return "", 200
        else:
            return "", 403

    @app.route("/api/loans/<id>", methods=["PUT"])  # ?
    def loan_edit_by_id(id):
        user_id = request.headers.get("Authorization")
        user = repositories["users"].get_user_by_id(user_id)
        if(user == None):
            return "", 403
        elif user.is_librarian == 1:
            body = request.json
            loan = Loan(**body)
            repositories["loans"].loan_edit(loan)
            return "", 200
        else:
            return "", 403

    @app.route("/api/categories", methods=["GET"])
    def get_categories():
        all_categories = repositories["categories"].get_categories()
        return object_to_json(all_categories)

    @app.route("/api/categories", methods=["PUT"])
    def modify_categories():
        user_id = request.headers.get("Authorization")
        user = repositories["users"].get_user_by_id(user_id)
        if(user == None):
            return "", 403
        elif user.is_librarian == 1:
            body = request.json
            book_id = body["book_id"]
            categories = body["categories"]
            repositories["categories"].delete_categories(book_id)
            repositories["books"].add_category(book_id, categories)
            return "", 200
        else:
            return "", 403

    return app
