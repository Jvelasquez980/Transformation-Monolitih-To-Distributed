from flask import Blueprint, jsonify
from models.user import User

admin = Blueprint('admin', __name__)

@admin.route('/api/admin/users')  # Asegúrate del slash inicial
def list_users():
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]
    return jsonify(user_list), 200
