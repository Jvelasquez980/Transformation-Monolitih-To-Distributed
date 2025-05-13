from datetime import timedelta
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from utils.auth_helpers import get_logged_user

# Inicialización de la app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # Para sesiones, flash, etc.
app.config['JWT_SECRET_KEY'] = 'super-secret-jwt'  # Útil si JWT se usara localmente
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)  # Solo necesario si usas JWT en esta capa (opcional)

# Importar blueprints (debe hacerse después de crear `app`)
from controllers.auth_controller import auth
from controllers.book_controller import book
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery
from controllers.admin_controller import admin

# Registrar blueprints
app.register_blueprint(auth)
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)
app.register_blueprint(admin)

# Ruta principal
@app.route('/')
def home():
    user = get_logged_user()    
    return render_template('home.html', current_user=user)

# Entry point
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
