from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
import requests
from utils.auth_helpers import get_logged_user

auth = Blueprint('auth', __name__)
AUTH_SERVICE_URL = 'http://auth-service:5000'  # Ajusta si usas otra ruta interna

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    user = get_logged_user()
    if user:
        flash('Ya estás autenticado.')
        return redirect(url_for('book.catalog'),current_user=user)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        res = requests.post(f'{AUTH_SERVICE_URL}/api/login', json={'email': email, 'password': password})

        if res.status_code == 200:
            data = res.json()
            token = data['access_token']
            user = data['user']

            # Crear la respuesta y adjuntar cookie segura
            response = make_response(redirect(url_for('book.catalog')))
            response.set_cookie(
                'access_token',
                token,
                httponly=True,
                secure=False,  # Solo funciona con HTTPS
                samesite='Lax',
                max_age=60 * 60  # 1 hora de expiración (ajustable)
            )
            return response
        else:
            flash('Login failed')
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        res = requests.post(f'{AUTH_SERVICE_URL}/api/register', json=data)

        if res.status_code == 201:
            return redirect(url_for('auth.login_page'))
        else:
            flash(res.json().get('message', 'Registration failed'))
    return render_template('register.html')


@auth.route('/logout')
def logout():
    user = get_logged_user()
    if not user:
        flash('No estás autenticado.')
        return redirect(url_for('auth.login_page'))
    response = make_response(redirect(url_for('auth.login_page')))
    response.set_cookie('access_token', '', expires=0)
    return response
