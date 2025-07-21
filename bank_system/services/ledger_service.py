from models import Customer, Loan
import math

def get_balance(bank_name, customer_name, emi_number):
    # Fetch the customer based on name and bank
    customer = Customer.query.filter_by(name=customer_name, bank_name=bank_name).first()
    if not customer:
        return {'error': 'Customer not found'}

    loan = Loan.query.filter_by(customer_id=customer.id, bank_name=bank_name).first()
    if not loan:
        return {'error': 'Loan not found'}

    # Calculate amount paid till given EMI number
    emis_paid = min(emi_number, loan.num_emis)
    amount_paid = emis_paid * loan.emi_amount

    # Add all lump sum payments till that EMI number
    lump_sum = sum(p.lump_sum_amount for p in loan.payments if p.emi_number <= emi_number)
    amount_paid += lump_sum

    amount_remaining = max(0, loan.total_amount - amount_paid)
    emis_remaining = 0 if amount_remaining == 0 else math.ceil(amount_remaining / loan.emi_amount)

    return {
        'bank': bank_name,
        'customer': customer_name,
        'amount_paid': int(amount_paid),
        'emis_remaining': emis_remaining
    }
