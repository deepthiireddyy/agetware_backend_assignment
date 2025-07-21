from models import db, Customer, Loan, Payment
import math

def process_payment(data):
    bank_name = data['bank_name']
    customer_name = data['customer_name']
    lump_sum_amount = float(data['lump_sum_amount'])
    emi_number = int(data['emi_no'])

    # Fetch customer
    customer = Customer.query.filter_by(name=customer_name, bank_name=bank_name).first()
    if not customer:
        return {"error": "Customer not found"}

    # Fetch loan
    loan_id = int(data['loan_id'])
    loan = Loan.query.filter_by(id=loan_id, customer_id=customer.id, bank_name=bank_name).first()
    if not loan:
        return {"error": "Loan not found for this customer and bank"}

    # Validate EMI number
    if emi_number < 1 or emi_number > loan.num_emis:
        return {"error": "Invalid EMI number"}

    # Check if a payment is already made at this EMI number
    existing_payment = Payment.query.filter_by(loan_id=loan.id, emi_number=emi_number).first()
    if existing_payment:
        return {
            "error": f"Lump sum already paid at EMI #{emi_number}",
            "payment_id": existing_payment.id,
            "paid_lump_sum": existing_payment.lump_sum_amount
        }

    # Add the new payment
    payment = Payment(
        emi_number=emi_number,
        lump_sum_amount=lump_sum_amount,
        customer_id=customer.id,
        loan_id=loan.id
    )
    db.session.add(payment)
    db.session.flush()

    # Fetch all payments for this loan
    all_payments = Payment.query.filter_by(loan_id=loan.id).all()

    # Calculate how many unique EMI payments have been made
    paid_emis = {p.emi_number for p in all_payments}
    emis_paid = len(paid_emis)

    # Calculate total lump sum paid
    lump_sum_total = sum(p.lump_sum_amount for p in all_payments)

    # Calculate total paid till now
    total_paid = (emis_paid * loan.emi_amount) + lump_sum_total

    # Calculate remaining amount
    amount_remaining = max(0, loan.total_amount - total_paid)

    # Update loan's remaining EMIs
    if amount_remaining <= 0:
        loan.emis_remaining = 0
        loan_closed = True
    else:
        loan.emis_remaining = math.ceil(amount_remaining / loan.emi_amount)
        loan_closed = False

    db.session.commit()

    return {
        "message": "Payment successful",
        "payment_id": payment.id,
        "loan_id": loan.id,
        "customer_name": customer.name,
        "bank_name": loan.bank_name,
        "emi_number_paid": emi_number,
        "lump_sum_paid_now": lump_sum_amount,
        "emi_amount": loan.emi_amount,
        "total_paid_till_now": round(total_paid, 2),
        "amount_remaining": round(amount_remaining, 2),
        "emis_remaining": loan.emis_remaining,
        "loan_closed": loan_closed,
        "created_at": payment.created_at.isoformat()
    }
