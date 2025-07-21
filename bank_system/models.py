from extensions import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('name', 'bank_name', name='_customer_bank_uc'),
    )

    def __repr__(self):
        return f"<Customer {self.name} at {self.bank_name}>"


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    principal = db.Column(db.Integer, nullable=False)
    no_of_years = db.Column(db.Integer, nullable=False)
    rate_of_interest = db.Column(db.Float, nullable=False)
    emi_amount = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    num_emis = db.Column(db.Integer, nullable=False)
    emis_remaining = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp

    payments = db.relationship('Payment', backref='loan', lazy=True)
    customer = db.relationship('Customer', backref=db.backref('loans', lazy=True))

    def __repr__(self):
        return f"<Loan {self.id}: {self.principal} for {self.no_of_years} years at {self.rate_of_interest}%>"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emi_number = db.Column(db.Integer, nullable=False)
    lump_sum_amount = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp

    customer = db.relationship('Customer', backref=db.backref('payments', lazy=True))
    # loan = db.relationship('Loan', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f"<Payment {self.id}: {self.lump_sum_amount} at EMI {self.emi_number}>"
