import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions import db
from models import Customer, Loan
from app import app

def initialize_database():
    with app.app_context():
        db.create_all()
        print("✅ Tables created successfully.")

        if not Customer.query.first():
            customer = Customer(name="Deepthi Reddy", bank_name="SBI")
            db.session.add(customer)
            db.session.commit()

            num_emis = 24
            loan = Loan(
                bank_name="SBI",
                customer_name="Deepthi Reddy",
                principal=50000,
                no_of_years=2,
                rate_of_interest=10,
                emi_amount=2300,
                total_amount=55200,
                num_emis=num_emis,
                emis_remaining=num_emis,  # ✅ Fix: required field
                customer_id=customer.id
            )
            db.session.add(loan)
            db.session.commit()

            print("🌱 Seed data inserted.")

if __name__ == "__main__":
    initialize_database()
