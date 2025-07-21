from flask import Flask, render_template
from extensions import db
from routes import lend_bp, payment_bp, ledger_bp, account_bp, admin_bp
import os

app = Flask(__name__, instance_relative_config=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(lend_bp, url_prefix='/lend')
app.register_blueprint(payment_bp, url_prefix='/payment')
app.register_blueprint(ledger_bp, url_prefix='/ledger')
app.register_blueprint(account_bp, url_prefix='/account')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
