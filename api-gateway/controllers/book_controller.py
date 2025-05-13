from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from utils.auth_helpers import get_logged_user  # Función auxiliar que obtiene al usuario autenticado

book = Blueprint('book', __name__)
BOOK_SERVICE_URL = 'http://book-service:5000'
USER_ID_HEADER = "X-User-Id"

@book.route('/catalog')
def catalog():
    """Muestra el catálogo completo de libros (público)."""
    response = requests.get(f'{BOOK_SERVICE_URL}/api/catalog')
    books = response.json() if response.status_code == 200 else []
    user = get_logged_user()
    return render_template('catalog.html', books=books, current_user=user)

@book.route('/my_books')
def my_books():
    """Muestra los libros del usuario autenticado."""
    user = get_logged_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    user_data = user
    user_id = user_data['id']

    # Pasamos el ID del usuario como parámetro o header (tú defines la convención)
    response = requests.get(f'{BOOK_SERVICE_URL}/api/my_books/{user_id}', headers={USER_ID_HEADER: str(user_id)})
    books = response.json() if response.status_code == 200 else []
    return render_template('my_books.html', books=books, current_user=user)

@book.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Permite al usuario autenticado agregar un nuevo libro."""
    user = get_logged_user()
    if not user:
        flash('Debes iniciar sesión para agregar un libro.')
        return redirect(url_for('auth.login_page'))

    user_data = user
    user_id = user_data['id']

    if request.method == 'POST':
        # Recoge datos del formulario
        data = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price')),
            'stock': int(request.form.get('stock')),
            'seller_id': user_id
        }
        response = requests.post(f'{BOOK_SERVICE_URL}/api/add_book', json=data, headers={USER_ID_HEADER: str(user_id)})
        if response.status_code == 201:
            return redirect(url_for('book.catalog'))
        flash('Error al agregar el libro.')
    return render_template('add_book.html', current_user=user)

@book.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """Permite al usuario autenticado editar su propio libro."""
    user = get_logged_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    user_data = user
    user_id = user_data['id']

    # Validar que el libro le pertenece al usuario
    response = requests.get(
        f'{BOOK_SERVICE_URL}/api/edit_book/{book_id}',
        headers={USER_ID_HEADER: str(user_id)}
    )
    if response.status_code != 200:
        flash('Error al obtener el libro.')
        return redirect(url_for('book.catalog'))

    book_to_edit = response.json()

    if book_to_edit['seller_id'] != user_id:
        return "No tienes permiso para editar este libro.", 403

    # Procesar la edición
    if request.method == 'POST':
        data = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price')),
            'stock': int(request.form.get('stock'))
        }
        response = requests.post(f'{BOOK_SERVICE_URL}/api/edit_book/{book_id}', json=data, headers={USER_ID_HEADER: str(user_id)})
        if response.status_code == 200:
            return redirect(url_for('book.catalog'))
        flash('Error al actualizar el libro.')

    return render_template('edit_book.html', book=book_to_edit, current_user=user)


@book.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """Permite al usuario autenticado eliminar su propio libro."""
    user = get_logged_user()
    if not user:
        return redirect(url_for('auth.login_page'))

    user_data = user
    user_id = user_data['id']
    # Realizar eliminación
    response = requests.post(f'{BOOK_SERVICE_URL}/api/delete_book/{book_id}' , headers = {
         USER_ID_HEADER: str(user_id)
}) 
    if response.status_code != 204:
        flash('Error al eliminar el libro.')
    return redirect(url_for('book.catalog'))
