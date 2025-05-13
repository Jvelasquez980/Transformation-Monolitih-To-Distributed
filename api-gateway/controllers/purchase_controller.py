from flask import Blueprint, request, redirect, url_for, flash
from utils.auth_helpers import get_logged_user
import requests
#from app import db
ORDER_SERVICE_URL = 'http://orders-service:5000'
BOOK_SERVICE_URL = 'http://book-service:5000'
USER_ID_HEADER = "X-User-Id"
purchase = Blueprint('purchase', __name__)

@purchase.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    user = get_logged_user()
    if not user:
        flash('Debes iniciar sesión para agregar un libro.')
        return redirect(url_for('auth.login_page'))

    user_data = user
    user_id = user_data['id']
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    book = requests.get(f'{BOOK_SERVICE_URL}/api/get_book/{book_id}', headers={USER_ID_HEADER: str(user_id)})
    if book.status_code != 200:
        flash('Error al obtener el libro.')
        return redirect(url_for('book.catalog'))
    book = book.json()
    new_purchase = requests.post(f'{ORDER_SERVICE_URL}/api/buy/{book_id}',headers={USER_ID_HEADER: str(user_id)} , json={ 'quantity': quantity, 'price': price, 'book': book})
    if new_purchase.status_code != 200:
        flash('Error al procesar la compra.')
        return redirect(url_for('book.catalog'))
    
    
    return redirect(url_for('payment.payment_page', purchase_id=new_purchase.json()['purchase_id']))
