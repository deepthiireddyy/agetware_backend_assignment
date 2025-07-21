from models import db, Loan, Customer

def lend_money(data):
    try:
        bank_name = data['bank_name']
        customer_name = data['customer_name']
        principal = data['principal']
        no_of_years = data['no_of_years']
        rate = data['rate_of_interest']

        customer = Customer.query.filter_by(name=customer_name).first()
        if not customer:
            return {'error': 'Customer does not exist'}

        total_amount = principal + (principal * rate * no_of_years) / 100
        num_emis = no_of_years * 12
        emi_amount = round(total_amount / num_emis)

        loan = Loan(
            bank_name=bank_name,
            customer_name=customer_name,
            principal=principal,
            no_of_years=no_of_years,
            rate_of_interest=rate,
            emi_amount=emi_amount,
            total_amount=total_amount,
            num_emis=num_emis,
            emis_remaining=num_emis,
            customer_id=customer.id
        )

        db.session.add(loan)
        db.session.commit()

        return {'message': f'Loan sanctioned to {customer_name} at {bank_name}'}
    except Exception as e:
        return {'error': str(e)}