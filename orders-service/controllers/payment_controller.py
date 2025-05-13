from flask import Blueprint, request, redirect, url_for, jsonify
from models.payment import Payment
from models.purchase import Purchase
from extensions import db
USER_ID_HEADER = "X-User-Id"

payment = Blueprint('payment', __name__)

@payment.route('/api/payment/<int:purchase_id>', methods=['GET', 'POST'])
def payment_page(purchase_id):
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return "Missing user_id", 401
    if request.method == 'POST':
        method = request.json.get('method')
        new_payment = Payment(purchase_id=purchase_id, amount=request.json.get('amount'), payment_method=method, payment_status='Paid')
        db.session.add(new_payment)
        purchase = Purchase.query.get(purchase_id)
        purchase.status = 'Paid'
        db.session.commit()
        return jsonify({"message": "Payment processed successfully", "purchase_id": purchase_id}), 200
    return jsonify({"message": "method not allowed"}), 405
