from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy.orm import Session
from database import engine
from models.Transaction import Transaction, load_transactions

app = Flask(__name__)

session = Session(engine)

@app.route('/', methods=["GET","POST"])
def get_home():
    transactions = load_transactions()
    return render_template('dashboard.html', transactions=transactions)
                           
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        newTransaction = Transaction(title=request.form.get('title'), amount=request.form.get('amount'), transactionDate=request.form.get('date'))
        session.add(newTransaction)
        try:
            session.commit()
        except:
            session.rollback()
        
        return redirect(url_for('get_home'))
    
# This is for the D3 example
@app.route('/get_data')
def get_data():
    # Process and prepare your data
    data = [{"label": "A", "value": 50}, {"label": "B", "value": 20}, {"label": "C", "value": 15}]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)