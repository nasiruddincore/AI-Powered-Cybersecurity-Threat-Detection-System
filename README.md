# 🛡️ AI-Powered Cybersecurity Threat Detection System

## 📌 Project Overview
An end-to-end Machine Learning system that acts as a virtual Security Operations Center (SOC) analyst. It ingests simulated real-time network traffic, analyzes packet behaviors, and uses an AI model (Random Forest) to instantly detect and block Zero-Day threats, DoS attacks, and Brute Force attempts.

## 🚀 Why This Matters (Industry Relevance)
Traditional static firewalls fail against modern, mutated cyberattacks. AI-driven anomaly detection is currently deployed by companies like CrowdStrike, Microsoft, and Palo Alto Networks to automatically classify threats in milliseconds rather than relying on human intervention.

## 🛠️ Tech Stack
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy
*   **Backend & API:** Python, Flask
*   **Simulation & Networking:** Python Requests module

## 🏗️ System Architecture
1. **Data Generator:** Synthesizes realistic corporate network logs.
2. **ML Engine:** Trains a Random Forest Classifier to distinguish normal vs. malicious patterns.
3. **Detection API:** A Flask-based endpoint serving the model in real-time.
4. **Threat Simulator:** Emulates hacking attempts (DoS, Brute Force) against the API.

## ⚙️ How to Run Locally

**1. Clone & Setup**
```bash
git clone [https://github.com/YOUR_USERNAME/AI-Cybersecurity-Threat-Detection.git](https://github.com/YOUR_USERNAME/AI-Cybersecurity-Threat-Detection.git)
cd AI-Cybersecurity-Threat-Detection
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt