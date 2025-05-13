from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth_helpers import get_logged_user
import requests
#from app import db
from flask_login import login_required
ORDER_SERVICE_URL = 'http://orders-service:5000'
USER_ID_HEADER = "X-User-Id"
payment = Blueprint('payment', __name__)

@payment.route('/payment/<int:purchase_id>', methods=['GET', 'POST'])
def payment_page(purchase_id):
    user = get_logged_user()
    if not user:
        flash('Debes iniciar sesión para realizar el pago.')
        return redirect(url_for('auth.login_page'))
    user_data = user
    user_id = user_data['id']
    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')
        response = requests.post(f'{ORDER_SERVICE_URL}/api/payment/{purchase_id}', headers={USER_ID_HEADER: str(user_id)}, json={'method': method, 'amount': amount})
        if response.status_code != 200:
            flash('Error al procesar el pago.')
            return redirect(url_for('book.catalog'))
        return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))
    return render_template('payment.html', purchase_id=purchase_id, current_user=user)