from flask import Flask
from extensions import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'

db.init_app(app)

from controllers.book_controller import book


app.register_blueprint(book)


if __name__ == '__main__':
# OJO este conexto crea las tablas e inicia los proveedores de entrega, 
# se debe ejecutar cada que se reinstala y ejecuta la aplicación Bookstore
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
