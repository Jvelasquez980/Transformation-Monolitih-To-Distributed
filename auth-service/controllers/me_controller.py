from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

me = Blueprint('me', __name__)

@me.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        # Verificación del encabezado Authorization
        authorization_header = request.headers.get('Authorization')
        # print(f"Authorization header: {authorization_header}", flush=True)
        
        # Extraer el token
        token = authorization_header.split(" ")[1] if authorization_header else None
        # print(f"Token extraído: {token}", flush=True)
        
        # Verificar si el token está presente
        if not token:
            raise ValueError("Token no encontrado en la solicitud")

        # Obtener el usuario a partir del JWT
        user_id = get_jwt_identity()
        # print(f"User ID extraído del JWT: {user_id}", flush=True)

        # Asegúrate de que el user_id sea válido
        if not user_id:
            raise ValueError("El usuario no está autenticado")

        user = User.query.get(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        }), 200

    except Exception as e:
        # Manejo de excepciones y logging
        print(f"[ERROR] {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 422