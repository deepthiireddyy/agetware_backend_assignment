# routes/payment.py
from flask import Blueprint, request, jsonify
from services.payment_service import process_payment

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/', methods=['POST'])
def make_payment():
    data = request.get_json()

    required_fields = ['bank_name', 'customer_name', 'lump_sum_amount', 'emi_no']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields in request"}), 400

    result = process_payment(data)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201
