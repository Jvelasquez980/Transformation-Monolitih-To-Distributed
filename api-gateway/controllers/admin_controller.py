import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.auth_helpers import get_logged_user

admin = Blueprint('admin', __name__)
AUTH_SERVICE_URL = 'http://auth-service:5000'
@admin.route('/admin/users')
def list_users():
    token = request.cookies.get('access_token')
    if not token or not get_logged_user():
        flash("Debes iniciar sesión para ver esta página.")
        return redirect(url_for('auth.login_page'))

    # Si el token es válido, continuar
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{AUTH_SERVICE_URL}/api/admin/users', headers=headers)

    users = response.json() if response.status_code == 200 else []
    user = get_logged_user()
    if not user:
        flash("Debes iniciar sesión para ver esta página.")
        return redirect(url_for('auth.login_page'))
    return render_template('list_users.html', users=users, current_user=user)
