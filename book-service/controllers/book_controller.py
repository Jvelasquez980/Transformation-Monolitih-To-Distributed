from flask import Blueprint, request, redirect, url_for, jsonify
from models.book import Book

from extensions import db
#from app import db

book = Blueprint('book', __name__)
USER_ID_HEADER = "X-User-Id"
#@book.route('/')
#@login_required
#def home():
#    return render_template('home.html')

#@book.route('/')
@book.route('/api/catalog')
def catalog():
    books = Book.query.all()
    books = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "price": book.price,
            "stock": book.stock
        }
        for book in books
    ]
    return jsonify(books), 200

@book.route('/api/my_books/<int:user_id>', methods=['GET'])
def my_books(user_id):
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 401
    books = Book.query.filter_by(seller_id=user_id).all()
    books = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "price": book.price,
            "stock": book.stock,
            "seller_id": book.seller_id
        }
        for book in books
    ]
    return jsonify(books)

@book.route('/api/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        user_id = request.headers.get(USER_ID_HEADER)
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 401
        title = request.json.get('title')
        author = request.json.get('author')
        description = request.json.get('description')
        price = float(request.json.get('price'))
        stock = int(request.json.get('stock'))
        new_book = Book(title=title, author=author, description=description, price=price, stock=stock, seller_id=user_id)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully"}), 201

@book.route('/api/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 401

    book_to_edit = Book.query.get_or_404(book_id)

    if str(book_to_edit.seller_id) != str(user_id):
        return jsonify({"error": "No tienes permiso para editar este libro."}), 403

    if request.method == 'POST':
        book_to_edit.title = request.json.get('title')
        book_to_edit.author = request.json.get('author')
        book_to_edit.description = request.json.get('description')
        book_to_edit.price = float(request.json.get('price'))
        book_to_edit.stock = int(request.json.get('stock'))

        db.session.commit()
        return jsonify({"message": "Libro actualizado correctamente."}), 200

    # Si es GET, retorna los datos del libro
    return jsonify({
        "id": book_to_edit.id,
        "title": book_to_edit.title,
        "author": book_to_edit.author,
        "description": book_to_edit.description,
        "price": book_to_edit.price,
        "stock": book_to_edit.stock,
        "seller_id": book_to_edit.seller_id
        
    }), 200


@book.route('/api/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 401
    book_to_delete = Book.query.get_or_404(book_id)
    print(book_to_delete.seller_id ,flush=True)
    print(book_to_delete.seller_id != user_id,flush=True)
    print(user_id,flush=True)
    if book_to_delete.seller_id != int(user_id):
        return "No tienes permiso para eliminar este libro.", 403

    db.session.delete(book_to_delete)
    db.session.commit()
    return jsonify({"message": "Libro eliminado correctamente."}), 204

@book.route('/api/get_book/<int:book_id>', methods=['GET'])
def get_quantity(book_id):
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 401
    book = Book.query.get_or_404(book_id)
    if book.stock <= 0:
        return jsonify({"error": "No hay stock disponible."}), 400
    else:
        book.stock -= 1

    db.session.commit()
    
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "price": book.price,
        "stock": book.stock
    }), 200
