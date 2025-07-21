from flask import Blueprint, request, jsonify
from models import db, Customer, Loan
import math

lend_bp = Blueprint('lend', __name__)

@lend_bp.route('/', methods=['POST'])
def lend_money():
    data = request.get_json()
    required_fields = ['bank_name', 'customer_name', 'principal', 'years', 'rate']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields in request'}), 400

    bank_name = data['bank_name']
    customer_name = data['customer_name']
    principal = float(data['principal'])
    no_of_years = int(data['years'])
    rate_of_interest = float(data['rate'])

    # Check if customer exists
    customer = Customer.query.filter_by(name=customer_name, bank_name=bank_name).first()
    if not customer:
        customer = Customer(name=customer_name, bank_name=bank_name)
        db.session.add(customer)
        db.session.commit()

    # Calculate interest and EMI
    total_interest = (principal * rate_of_interest * no_of_years) / 100
    total_amount = principal + total_interest
    num_emis = no_of_years * 12
    emi_amount = math.ceil(total_amount / num_emis)

    # Create loan
    loan = Loan(
        bank_name=bank_name,
        customer_name=customer_name,
        principal=principal,
        no_of_years=no_of_years,
        rate_of_interest=rate_of_interest,
        emi_amount=emi_amount,
        total_amount=total_amount,
        num_emis=num_emis,
        emis_remaining=num_emis,
        customer_id=customer.id
    )
    db.session.add(loan)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Loan created successfully',
        'customer_id': customer.id,
        'loan_id': loan.id,
        'bank_name': loan.bank_name,
        'customer_name': loan.customer_name,
        'principal': round(principal, 2),
        'rate_of_interest': rate_of_interest,
        'no_of_years': no_of_years,
        'total_interest': round(total_interest, 2),
        'total_amount': round(total_amount, 2),
        'num_emis': num_emis,
        'emi_amount': emi_amount,
        'emis_remaining': num_emis,
        'created_at': loan.created_at.isoformat()
    }), 200
