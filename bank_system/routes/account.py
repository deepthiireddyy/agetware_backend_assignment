from flask import Blueprint, request, jsonify
from models import db, Customer, Loan, Payment
import math

account_bp = Blueprint('account', __name__)

@account_bp.route('/overview', methods=['GET'])
def loan_overview():
    bank_name = request.args.get('bank_name')
    customer_name = request.args.get('customer_name')
    status_filter = request.args.get('status')  # can be 'active' or 'closed' (optional)

    if not bank_name or not customer_name:
        return jsonify({'error': 'Bank name and customer name are required'}), 400

    # Ensure customer is matched with bank too
    customer = Customer.query.filter_by(name=customer_name, bank_name=bank_name).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    # Get all loans for the bank & customer
    loans = Loan.query.filter_by(customer_id=customer.id, bank_name=bank_name).all()

    # Optional filtering
    if status_filter == 'active':
        loans = [loan for loan in loans if loan.emis_remaining > 0]
    elif status_filter == 'closed':
        loans = [loan for loan in loans if loan.emis_remaining == 0]

    if not loans:
        return jsonify({'error': 'No loans found for this customer at the specified bank'}), 404

    overview = []
    for loan in loans:
        P = loan.principal
        r = loan.rate_of_interest
        t = loan.no_of_years

        I = P * r * t / 100
        A = P + I
        total_emis = t * 12
        emi_amount = math.ceil(A / total_emis)

        total_paid = sum(p.lump_sum_amount for p in loan.payments)
        total_paid += (loan.num_emis - loan.emis_remaining) * loan.emi_amount

        loan_summary = {
            'loan_id': loan.id,
            'bank_name': loan.bank_name,
            'customer_name': loan.customer_name,
            'principal': round(P, 2),
            'rate_of_interest': round(r, 2),
            'no_of_years': t,
            'total_interest': round(I, 2),
            'total_amount': round(A, 2),
            'emi_amount': round(emi_amount, 2),
            'num_emis': total_emis,
            'emis_paid': loan.num_emis - loan.emis_remaining,
            'emis_remaining': loan.emis_remaining,
            'amount_paid_till_date': round(total_paid, 2),
            'loan_closed': loan.emis_remaining == 0
        }

        overview.append(loan_summary)

    return jsonify({
        'customer_id': customer.id,
        'customer_name': customer.name,
        'loans': overview
    }), 200
