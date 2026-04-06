import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# CONFIGURATION: Put your Gemini API Key in a .env file as GEMINI_API_KEY=AIza...
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_context_explanation(transaction_data, prediction_data):
    """
    Detailed contextual analysis using Google Gemini.
    """
    if not GEMINI_API_KEY:
        # Fallback to smart stub if no key is provided
        return _generate_mock_explanation(transaction_data, prediction_data)

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Construct a detailed prompt with all available data
        prompt = f"""
        Analyze this financial transaction for potential fraud:
        - Amount: ₹{transaction_data.get('amount')}
        - Sender: {transaction_data.get('nameOrig')} (Old Balance: {transaction_data.get('oldbalanceOrg')}, New: {transaction_data.get('newbalanceOrig')})
        - Receiver: {transaction_data.get('nameDest')} (Old Balance: {transaction_data.get('oldbalanceDest')}, New: {transaction_data.get('newbalanceDest')})
        - Transaction Type: {transaction_data.get('type')}
        
        AI Ensemble Consensus:
        - Overall Fraud Probability: {prediction_data.get('probability')}%
        - Decision: {'FRAUD' if prediction_data.get('is_fraud') else 'Normal'}
        - Model Breakdown: {prediction_data.get('model_breakdown')}
        
        SHAP Feature Importance:
        {prediction_data.get('shap_values')}
        
        Task: Provide a concise, professional explanation of why this transaction was flagged (or verified) and what the primary risk factors are. Use a confident, analytic tone. Keep response under 100 words.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"Gemini Analysis unavailable: {str(e)}. Fallback: " + _generate_mock_explanation(transaction_data, prediction_data)

def _generate_mock_explanation(transaction_data, prediction_data):
    is_fraud = prediction_data.get("is_fraud")
    prob = prediction_data.get("probability")
    amount = transaction_data.get("amount", "0")
    
    ensemble_breakdown = ", ".join([f"{m['name']} ({m['prob']}%)" for m in prediction_data.get("model_breakdown", [])])
    shap_vals = prediction_data.get("shap_values", [])
    top_feature = shap_vals[0].get("feature", "Unknown") if shap_vals else "Unknown"
    second_feature = shap_vals[1].get("feature", "Unknown") if len(shap_vals) > 1 else ""
    
    reason = f"Primary driving features were '{top_feature}'"
    if second_feature:
        reason += f" and '{second_feature}'"
        
    if is_fraud:
        return f"🚨 ALERT: High Risk Fraud Detected. Ensemble Consensus: {prob}% risk. Models: {ensemble_breakdown}. {reason}. Recommendation: REJECT."
    elif prob > 30:
        return f"⚠️ WARNING: Elevated Risk Found. Consensus: {prob}% risk. {reason}. Recommendation: MANUAL REVIEW."
    else:
        return f"✅ SUCCESS: Transaction Verified. Consensus: {prob}% risk. {reason}. Recommendation: APPROVE."
