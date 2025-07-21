# BANK LOAN MANAGEMENT SYSTEM
A Flask based web application to manage bank loans, payments, and account overviews for customers and banks. The system allows banks to lend money, customers to make payments, and both to track loan balances and EMIs. It features a modern web UI and uses SQLite for data storage.

# FEATURES
- **Lend Money:** Banks can create new loans for customers, specifying principal, interest rate, and duration.
- **Make Payments:** Customers can make lump sum payments or regular EMIs towards their loans.
- **Check Balance:** View the amount paid and EMIs remaining for any loan.
- **Account Overview:** Get a summary of all loans for a customer at a bank.
-- **Web Interface:** User-friendly forms for all operations.

# TECH STACK
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS/JavaScript (frontend)

# SETUP INSTRUCTIONS
- Open new terminal in VScode and follow the below instructions.

1. **Setup Virtual Environment:**

    python -m venv venv

2. **Activate Virtual Environment:**

    - Windows:
        venv\Scripts\activate
    
    - macOS/Linux:
        source venv/bin/activate

3. **Install dependencies:**

    pip install -r requirements.txt

4. **Initialize the database:**

    python create_db.py

    To seed with sample data (optional):
        python databse/init_db.py

5. **Run the application:**

    python app.py

6. **Open your browser:**

    Click on the url and open the browser.

# USAGE
- Use the web forms to lend money, make payments, check balances, and view account overviews.
- All data is stored in **instance/bank.db** (SQLite).

# PROJECT STRUCTURE
database/init_db.py         # (Optional) Seed Sample data
instance/bank.db            # Database
routes/                     # Flask blueprints for API endpoints
services/                   # Business logic for loans, payments, ledgers
static/                     # frontend JS and CSS
templates/                  # HTML template
app.py                      # Main Flask app
config.py                   # Configuration
create_db.py                # Script to create DB tables
extensions.py               # Initializes Flask extensions
models.py                   # SQLAlchemy models
requirements.txt            # Python dependencies
README.md                   # User Guide

# AUTHOR
- Deepthi Kumari Rayapureddy

# LICENSE
- Assignment purpose assigned by AgetWare.