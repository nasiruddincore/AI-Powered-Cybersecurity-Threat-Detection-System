import requests
import time
import random

API_URL = "http://127.0.0.1:5000/predict"

def generate_payload(scenario):
    if scenario == "normal_user":
        return {
            "packet_size": random.randint(100, 1500),
            "login_attempts": random.randint(1, 2),
            "connection_duration": random.randint(1, 60),
            "error_rate": round(random.uniform(0.0, 0.05), 3)
        }
    elif scenario == "dos_attack":
        # Huge packet sizes and long connection times
        return {
            "packet_size": random.randint(5000, 10000),
            "login_attempts": 1,
            "connection_duration": random.randint(200, 500),
            "error_rate": round(random.uniform(0.7, 0.9), 3)
        }
    elif scenario == "brute_force_attack":
        # Rapid failed login attempts
        return {
            "packet_size": random.randint(50, 150),
            "login_attempts": random.randint(20, 60),
            "connection_duration": random.randint(5, 20),
            "error_rate": round(random.uniform(0.8, 1.0), 3)
        }

print("=== INITIATING VIRTUAL CYBER THREAT SIMULATION ===\n")

# A mix of normal behavior and sudden attacks
traffic_scenarios = [
    "normal_user", 
    "normal_user", 
    "brute_force_attack", 
    "normal_user", 
    "dos_attack"
]

for i, scenario in enumerate(traffic_scenarios, 1):
    payload = generate_payload(scenario)
    print(f"[{i}] Simulating {scenario.upper().replace('_', ' ')}...")
    print(f"    -> Outgoing Network Traffic: {payload}")
    
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        print(f"    <- [AI SECURITY RESPONSE] Status: {result['status']} | Confidence: {result['threat_probability_score']}% | Action: {result['recommended_action']}\n")
    except Exception as e:
        print(f"    [ERROR] API not responding. Ensure app.py is running.\n")
        
    time.sleep(2) # Wait 2 seconds between requests