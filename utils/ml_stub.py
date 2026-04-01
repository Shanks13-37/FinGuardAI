import json
import random

def get_fraud_prediction(transaction_data):
    """
    Mock ML model prediction and explainability (SHAP/Captum).
    In a real scenario, this would load models like `models/lstm_model.pt` or `models/rf_model.pkl`.
    """
    # Simple heuristic to make the stub somewhat dynamic based on amount
    amount = float(transaction_data.get('amount', 0))
    
    # Base probability calculation
    if amount > 50000:
        base_prob = random.uniform(0.75, 0.99)
    elif amount > 10000:
        base_prob = random.uniform(0.3, 0.75)
    else:
        base_prob = random.uniform(0.01, 0.20)
        
    # Simulate 4 distinct ML models
    models_breakdown = [
        {"name": "Random Forest", "prob": max(0.0, min(1.0, base_prob + random.uniform(-0.1, 0.1)))},
        {"name": "LSTM Matrix", "prob": max(0.0, min(1.0, base_prob + random.uniform(-0.15, 0.15)))},
        {"name": "XGBoost", "prob": max(0.0, min(1.0, base_prob + random.uniform(-0.05, 0.05)))},
        {"name": "Isolation Forest", "prob": max(0.0, min(1.0, base_prob + random.uniform(-0.2, 0.2)))}
    ]
    
    # Calculate ensemble
    ensemble_prob = sum(m['prob'] for m in models_breakdown) / len(models_breakdown)
    is_fraud = ensemble_prob >= 0.65

    # Mock feature importances (SHAP values)
    features = ['Location Mismatch', 'Unusual Time', 'High Velocity', 'Large Amount', 'New Payee']
    feature_importances = []
    
    if is_fraud:
        # Heavily weight amount and velocity if fraud
        weights = [random.uniform(0.1, 0.3) for _ in range(5)]
        weights[3] = random.uniform(0.4, 0.7) # Amount
        weights[2] = random.uniform(0.2, 0.5) # Velocity
    else:
        # Uniform low weights if not fraud
        weights = [random.uniform(0.01, 0.1) for _ in range(5)]
        
    # Normalize weights
    total_weight = sum(weights)
    weights = [w/total_weight for w in weights]
    
    for i, f in enumerate(features):
        feature_importances.append({
            "feature": f,
            "importance": round(weights[i] * 100, 2)
        })
        
    # Sort by importance descending
    feature_importances.sort(key=lambda x: x['importance'], reverse=True)

    # Round individual model probabilities
    for m in models_breakdown:
        m['prob'] = round(m['prob'] * 100, 2)
        
    return {
        "is_fraud": is_fraud,
        "probability": round(ensemble_prob * 100, 2),
        "model_breakdown": models_breakdown,
        "shap_values": feature_importances
    }
