from flask import Flask, render_template, request, jsonify
from utils.ml_stub import get_fraud_prediction
from utils.llm_stub import generate_context_explanation
import random

app = Flask(__name__)

@app.route('/')
def user_dashboard():
    """Renders the main User/Customer interface for transaction requests."""
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    """Renders the Analytics & Reports monitor for admins."""
    return render_template('admin.html')

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
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
