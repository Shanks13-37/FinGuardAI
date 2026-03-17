import os
from dotenv import load_dotenv

load_dotenv()

def generate_context_explanation(transaction_data, prediction_data):
    """
    Mock OpenAI GPT API call.
    In a real scenario, this would use the OPENAI_API_KEY from .env
    and call the OpenAI API with prompt engineering.
    """
    # api_key = os.getenv("OPENAI_API_KEY") 
    
    is_fraud = prediction_data.get("is_fraud")
    prob = prediction_data.get("probability")
    amount = transaction_data.get("amount", "0")
    recipient = transaction_data.get("recipient", "Unknown")
    
    top_feature = prediction_data.get("shap_values", [{}])[0].get("feature", "Unknown")
    
    if is_fraud:
        return f"ALERT: High risk of fraud ({prob}%). This transaction of ₹{amount} to {recipient} is suspicious primarily due to '{top_feature}'. We recommend pausing this transaction and verifying with the recipient immediately."
    elif prob > 30:
        return f"WARNING: Moderate risk ({prob}%). This transaction of ₹{amount} is slightly anomalous based on '{top_feature}'. Please review carefully before proceeding."
    else:
        return f"SUCCESS: Normal transaction. The transfer of ₹{amount} to {recipient} fits your typical spending patterns. No anomalous features detected."
