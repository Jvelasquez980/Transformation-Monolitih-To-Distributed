from flask import Blueprint, request, jsonify
from models.delivery import DeliveryProvider
from extensions import db
from models.delivery_assignment import DeliveryAssignment
USER_ID_HEADER = "X-User-Id"

delivery = Blueprint('delivery', __name__)

@delivery.route('/api/delivery/<int:purchase_id>', methods=['GET', 'POST'])
def select_delivery(purchase_id):
    user_id = request.headers.get(USER_ID_HEADER)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 401
    if request.method == 'POST':
        selected_provider_id = request.json.get('provider')
        
        new_assignment = DeliveryAssignment(purchase_id=purchase_id, provider_id=selected_provider_id)
        db.session.add(new_assignment)
        db.session.commit()
        
        return jsonify({"message": "Delivery provider assigned successfully", "purchase_id": purchase_id}), 200
    providers = DeliveryProvider.query.all()
    return jsonify([{
        "id": provider.id,
        "name": provider.name,
        "coverage_area": provider.coverage_area,
        "cost": provider.cost
    } for provider in providers]), 200