# 🛡️ AI-Powered Cybersecurity Threat Detection System

## 📌 Project Overview
An end-to-end Machine Learning system that acts as a virtual Security Operations Center (SOC) analyst. It ingests simulated real-time network traffic, analyzes packet behaviors, and uses an AI model (Random Forest) to instantly detect and block Zero-Day threats, DoS attacks, and Brute Force attempts. 

With the latest update, the project features a **real-time Streamlit UI dashboard** that visualizes network anomalies, tracks API confidence scores, and generates live security alerts.

## 🚀 Why This Matters (Industry Relevance)
Traditional static firewalls fail against modern, mutated cyberattacks. AI-driven anomaly detection is currently deployed by companies like CrowdStrike, Microsoft, and Palo Alto Networks to automatically classify threats in milliseconds rather than relying on human intervention.

## 🛠️ Tech Stack
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy
*   **Backend API:** Python, Flask
*   **Frontend Dashboard:** Streamlit, Plotly
*   **Simulation & Networking:** Python Requests

## 🏗️ System Architecture
1. **Data Generator:** Synthesizes realistic corporate network logs (Normal, DoS, Brute Force).
2. **ML Engine:** Trains a Random Forest Classifier to distinguish normal vs. malicious patterns.
3. **Detection API:** A Flask-based REST endpoint serving the ML model in real-time.
4. **Streamlit Dashboard:** A live-updating UI that polls the API, injects traffic, and plots threat metrics dynamically.

## 📁 Repository Structure
```text
AI-Cybersecurity-Threat-Detection/
│
├── data/                  # Generated network traffic CSV
├── models/                # Trained Random Forest (.pkl)
├── src/                   
│   ├── data_generator.py  # Script to synthesize training data
│   ├── train_model.py     # ML training and evaluation script
│   └── simulate_attacks.py# Terminal-based attack simulator
├── app.py                 # Flask Backend API
├── dashboard.py           # Streamlit Frontend UI
├── requirements.txt       # Project dependencies
└── README.md
