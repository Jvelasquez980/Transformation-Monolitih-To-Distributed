from flask import Blueprint, request, jsonify
from models.purchase import Purchase
from extensions import db
USER_ID_HEADER = "X-User-Id"
purchase = Blueprint('purchase', __name__)

@purchase.route('/api/buy/<int:book_id>', methods=['POST'])
def buy(book_id):   
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return "Missing user_id", 401

    book = request.json.get('book')
    quantity = int(request.json.get('quantity'))
    price = float(request.json.get('price'))
    if book['stock'] < quantity:
        return "No hay suficiente stock disponible.", 400

    total_price = price * quantity

    new_purchase = Purchase(
        user_id=user_id,
        book_id=book_id,
        quantity=quantity,
        total_price=total_price,
        status='Pending Payment'
    )
    
    db.session.add(new_purchase)
    db.session.commit()

    return jsonify({"message": "Compra realizada con éxito", "purchase_id": new_purchase.id}), 200
