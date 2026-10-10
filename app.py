from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained ML model
try:
    model = joblib.load('models/rf_model.pkl')
except FileNotFoundError:
    print("Model not found. Please run src/train_model.py first.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from incoming request
        data = request.json
        
        # Format data for the model
        features = np.array([[
            data['packet_size'],
            data['login_attempts'],
            data['connection_duration'],
            data['error_rate']
        ]])
        
        # Predict using AI
        prediction = model.predict(features)
        probability = model.predict_proba(features)[0][1] # Probability of being an attack
        
        is_threat = bool(prediction[0])
        status = "THREAT DETECTED" if is_threat else "NORMAL TRAFFIC"
        
        # Generate automated action alert
        return jsonify({
            'status': status,
            'threat_probability_score': round(probability * 100, 2),
            'recommended_action': 'BLOCK_IP_ADDRESS' if is_threat else 'ALLOW'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting AI Threat Detection API...")
    app.run(port=5000, debug=True)