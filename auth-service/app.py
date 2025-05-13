from flask import Flask
from extensions import db
from models.user import User
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['JWT_SECRET_KEY'] = 'super-secret-jwt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'

db.init_app(app)
jwt = JWTManager(app)
@app.errorhandler(Exception)
def handle_all_errors(e):
    import traceback
    print("[ERROR DETECTADO]", flush=True)
    traceback.print_exc()  # Imprime el stack trace completo
    return jsonify({"error": str(e)}), 500
print("[CONFIG] JWT_SECRET_KEY:", app.config.get("JWT_SECRET_KEY"), flush=True)

# Importar y registrar Blueprints
from controllers.auth_controller import auth
from controllers.admin_controller import admin
from controllers.me_controller import me

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(me)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
