from flask import Blueprint, request, jsonify
from models import db, Customer, Loan
import math

ledger_bp = Blueprint('ledger', __name__)

@ledger_bp.route('/', methods=['GET'])
def ledger():
    bank_name = request.args.get('bank_name')
    customer_name = request.args.get('customer_name')
    loan_id = request.args.get('loan_id')

    if not bank_name or not customer_name or not loan_id:
        return jsonify({"error": "Missing bank name, customer name or loan_id"}), 400

    customer = Customer.query.filter_by(name=customer_name, bank_name=bank_name).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    loan = Loan.query.filter_by(id=loan_id, customer_id=customer.id, bank_name=bank_name).first()
    if not loan:
        return jsonify({"error": f"Loan ID {loan_id} not found for {customer_name} at {bank_name}"}), 404

    # Regular EMIs paid = total EMIs - EMIs remaining
    emis_paid = loan.num_emis - loan.emis_remaining
    regular_emi_paid = emis_paid * loan.emi_amount

    # Lump sum paid
    lump_sum = sum(p.lump_sum_amount for p in loan.payments)

    # Total paid till now
    total_paid = regular_emi_paid + lump_sum

    # Amount remaining
    amount_remaining = max(0, loan.total_amount - total_paid)
    emis_remaining = loan.emis_remaining

    return jsonify({
        "bank_name": bank_name,
        "customer_name": customer_name,
        "loan_id": loan.id,
        "principal": loan.principal,
        "rate_of_interest": loan.rate_of_interest,
        "no_of_years": loan.no_of_years,
        "total_interest": round(loan.total_amount - loan.principal, 2),
        "total_amount": round(loan.total_amount, 2),
        "emi_amount": loan.emi_amount,
        "num_emis": loan.num_emis,
        "loan_closed": emis_remaining == 0,
        "transactions": [
            {
                "emi_number": p.emi_number,
                "lump_sum_amount": p.lump_sum_amount,
                "paid_at": p.created_at.isoformat()
            } for p in sorted(loan.payments, key=lambda x: x.emi_number)
        ]
    })
