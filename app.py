from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from utils.ml_stub import get_fraud_prediction
from utils.llm_stub import generate_context_explanation
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Global in-memory list to track transactions during app runtime
transactions = []

@app.route('/')
def user_dashboard():
    """Renders the main User/Customer interface for transaction requests."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles admin login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Handles admin logout."""
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    """Renders the Analytics & Reports monitor for admins."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
        
    # Calculate stats
    total_tx = len(transactions)
    flagged = sum(1 for tx in transactions if tx.get('prediction', {}).get('is_fraud'))
    
    return render_template('admin.html', 
                           total_tx=total_tx, 
                           flagged=flagged,
                           recent_transactions=list(reversed(transactions))[-10:])

@app.route('/api/transaction', methods=['POST'])
def handle_transaction():
    """API endpoint to process a transaction and return fraud analysis."""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    # 1. Get ML Prediction and Explainability (SHAP)
    prediction = get_fraud_prediction(data)
    
    # 2. Get LLM Context based on AI suggestion
    explanation = generate_context_explanation(data, prediction)
    
    # Simulate a transaction ID
    tx_id = f"TXN{random.randint(1000000, 9999999)}"
    
    response_data = {
        "transaction_id": tx_id,
        "amount": data.get("amount"),
        "recipient": data.get("recipient"),
        "prediction": prediction,
        "explanation": explanation
    }
    
    # Store transaction for admin dashboard
    transactions.append(response_data)
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
