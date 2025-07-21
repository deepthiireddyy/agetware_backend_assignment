# routes/admin.py
from flask import Blueprint, request, jsonify
from models import db, Loan

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/loans', methods=['GET'])
def all_loans():
    bank_name = request.args.get('bank_name')
    loan_status = request.args.get('loan_status')  # 'open' or 'closed'

    query = Loan.query

    if bank_name:
        query = query.filter_by(bank_name=bank_name)

    loans = query.all()
    results = []

    for loan in loans:
        loan_closed = loan.emis_remaining == 0
        if loan_status:
            if loan_status == 'open' and loan_closed:
                continue
            if loan_status == 'closed' and not loan_closed:
                continue

        results.append({
            "loan_id": loan.id,
            "customer_name": loan.customer_name,
            "bank_name": loan.bank_name,
            "principal": loan.principal,
            "total_amount": loan.total_amount,
            "rate_of_interest": loan.rate_of_interest,
            "no_of_years": loan.no_of_years,
            "emi_amount": loan.emi_amount,
            "emis_remaining": loan.emis_remaining,
            "status": "closed" if loan_closed else "open"
        })

    return jsonify({
        "total_loans": len(results),
        "filtered_by": {
            "bank_name": bank_name,
            "loan_status": loan_status
        },
        "loans": results
    })

@admin_bp.route('/analytics', methods=['GET'])
def loan_analytics():
    loans = Loan.query.all()

    total_loans = len(loans)
    total_principal = sum(loan.principal for loan in loans)
    total_interest = sum((loan.principal * loan.rate_of_interest * loan.no_of_years) / 100 for loan in loans)
    total_amount_expected = total_principal + total_interest
    avg_interest_rate = round(sum(loan.rate_of_interest for loan in loans) / total_loans, 2) if total_loans > 0 else 0

    total_paid = 0
    total_closed_loans = 0

    for loan in loans:
        if loan.emis_remaining == 0:
            total_closed_loans += 1
        # EMI paid
        paid_emi_amount = (loan.num_emis - loan.emis_remaining) * loan.emi_amount
        # Lump sums
        lump_sum_paid = sum(p.lump_sum_amount for p in loan.payments)
        total_paid += paid_emi_amount + lump_sum_paid

    return jsonify({
        "total_loans": total_loans,
        "total_closed_loans": total_closed_loans,
        "total_principal_disbursed": round(total_principal, 2),
        "total_interest_expected": round(total_interest, 2),
        "total_amount_expected": round(total_amount_expected, 2),
        "total_amount_paid": round(total_paid, 2),
        "average_interest_rate": avg_interest_rate
    })
