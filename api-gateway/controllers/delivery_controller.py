from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from utils.auth_helpers import get_logged_user  
ORDER_SERVICE_URL = 'http://orders-service:5000'
USER_ID_HEADER = "X-User-Id"

delivery = Blueprint('delivery', __name__)

@delivery.route('/delivery/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    user = get_logged_user()
    if not user:
        flash('Debes iniciar sesión para seleccionar un proveedor de entrega.')
    if request.method == 'POST':
        selected_provider_id = request.form.get('provider')
        response = requests.post(f'{ORDER_SERVICE_URL}/api/delivery/{purchase_id}', json={'provider_id': selected_provider_id}, headers={USER_ID_HEADER: str(user['id'])})
        if response.status_code != 200:
            flash('Error al asignar el proveedor de entrega.')
            return redirect(url_for('book.catalog'))
        flash('Proveedor de entrega asignado correctamente.')
        return redirect(url_for('book.catalog'))
    
    response = requests.get(f'{ORDER_SERVICE_URL}/api/delivery/{purchase_id}', headers={USER_ID_HEADER: str(user['id'])})
    if response.status_code != 200:
        flash('Error al obtener las opciones de entrega.')
        return redirect(url_for('book.catalog'))
    providers = response
    return render_template('delivery_options.html', providers=providers.json(), purchase_id=purchase_id, current_user=user)