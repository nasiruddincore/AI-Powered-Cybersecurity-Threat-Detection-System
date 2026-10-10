import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
from collections import deque
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SOC AI Threat Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# API Endpoint (Must match your running app.py)
API_URL = "http://127.0.0.1:5000/predict"

# --- SESSION STATE ---
# We use deque to keep the last 50 events for real-time graphs
if 'history' not in st.session_state:
    st.session_state.history = deque(maxlen=50)
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'total_scanned' not in st.session_state:
    st.session_state.total_scanned = 0
if 'threats_blocked' not in st.session_state:
    st.session_state.threats_blocked = 0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# --- HEADER ---
st.title("🛡️ AI-Powered Security Operations Center (SOC)")
st.markdown("Real-time network traffic analysis and Zero-Day threat detection.")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    
    # Toggle for running the simulation
    if st.button("▶️ Start Simulation" if not st.session_state.is_running else "⏸️ Pause Simulation"):
        st.session_state.is_running = not st.session_state.is_running
        
    st.markdown("---")
    st.subheader("Inject Custom Traffic")
    
    # Manual injection controls
    sim_type = st.selectbox("Select Traffic Type", ["Normal User", "DoS Attack", "Brute Force"])
    if st.button("Inject Traffic Now"):
        # Temporarily force an injection outside the loop
        manual_payload = None
        if sim_type == "Normal User":
             manual_payload = {"packet_size": 500, "login_attempts": 1, "connection_duration": 10, "error_rate": 0.01}
        elif sim_type == "DoS Attack":
             manual_payload = {"packet_size": 8500, "login_attempts": 1, "connection_duration": 400, "error_rate": 0.85}
        elif sim_type == "Brute Force":
             manual_payload = {"packet_size": 120, "login_attempts": 45, "connection_duration": 8, "error_rate": 0.95}
             
        try:
            res = requests.post(API_URL, json=manual_payload)
            result = res.json()
            st.session_state.history.append({
                "time": pd.Timestamp.now().strftime("%H:%M:%S"),
                "status": result["status"],
                "confidence": result["threat_probability_score"],
                "packet_size": manual_payload["packet_size"]
            })
            if result["status"] == "THREAT DETECTED":
                st.session_state.alerts.insert(0, f"⚠️ [MANUAL INJECTION] {sim_type} Blocked! Confidence: {result['threat_probability_score']}%")
                st.session_state.threats_blocked += 1
            st.session_state.total_scanned += 1
            st.success("Traffic injected successfully!")
        except Exception:
            st.error("API is offline. Please run app.py")

# --- METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)
metric_scanned = col1.empty()
metric_blocked = col2.empty()
metric_safe = col3.empty()
metric_status = col4.empty()

# --- CHARTS ROW ---
col_chart1, col_chart2 = st.columns(2)
chart_placeholder1 = col_chart1.empty()
chart_placeholder2 = col_chart2.empty()

# --- ALERTS SECTION ---
st.subheader("🚨 Recent Security Alerts (Threats Blocked)")
alerts_placeholder = st.empty()


# --- HELPER FUNCTIONS ---
def generate_random_payload():
    """Generates random traffic to simulate continuous network activity"""
    scenario = random.choices(["normal", "dos", "brute_force"], weights=[0.8, 0.1, 0.1])[0]
    if scenario == "normal":
        return {"packet_size": random.randint(100, 1500), "login_attempts": random.randint(1, 2), "connection_duration": random.randint(1, 60), "error_rate": round(random.uniform(0.0, 0.05), 3)}, "Normal"
    elif scenario == "dos":
        return {"packet_size": random.randint(5000, 10000), "login_attempts": 1, "connection_duration": random.randint(200, 500), "error_rate": round(random.uniform(0.7, 0.9), 3)}, "DoS"
    else:
        return {"packet_size": random.randint(50, 150), "login_attempts": random.randint(20, 60), "connection_duration": random.randint(5, 20), "error_rate": round(random.uniform(0.8, 1.0), 3)}, "Brute Force"

def update_ui():
    """Updates the Streamlit UI with the latest data in session_state"""
    
    # Update Metrics
    metric_scanned.metric("Total Packets Scanned", st.session_state.total_scanned)
    metric_blocked.metric("Threats Blocked", st.session_state.threats_blocked)
    safe_traffic = st.session_state.total_scanned - st.session_state.threats_blocked
    metric_safe.metric("Safe Traffic", safe_traffic)
    
    sys_status = "🟢 ACTIVE" if st.session_state.is_running else "⏸️ PAUSED"
    metric_status.metric("System Status", sys_status)

    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        
        # Line Chart: Threat Confidence over Time
        fig1 = px.line(df, x="time", y="confidence", title="Live Threat Confidence Score (%)", markers=True, 
                       color_discrete_sequence=['red'])
        fig1.update_layout(yaxis_range=[0, 100], xaxis_title="Time", yaxis_title="AI Confidence (%)")
        chart_placeholder1.plotly_chart(fig1, use_container_width=True)
        
        # Scatter Plot: Packet Size vs Status
        fig2 = px.scatter(df, x="time", y="packet_size", color="status", title="Network Traffic Anomaly Monitor",
                          color_discrete_map={"NORMAL TRAFFIC": "green", "THREAT DETECTED": "red"}, size_max=15)
        fig2.update_layout(xaxis_title="Time", yaxis_title="Packet Size (Bytes)")
        chart_placeholder2.plotly_chart(fig2, use_container_width=True)

    # Update Alerts List
    if st.session_state.alerts:
        # Show top 5 recent alerts
        alert_text = "\n\n".join([f"- {msg}" for msg in st.session_state.alerts[:5]])
        alerts_placeholder.error(alert_text)
    else:
        alerts_placeholder.success("No threats detected recently. Network is secure.")

# --- MAIN SIMULATION LOOP ---
# This runs constantly when is_running is True
if st.session_state.is_running:
    # Do one tick of simulation
    payload, true_label = generate_random_payload()
    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        # Update State
        st.session_state.total_scanned += 1
        st.session_state.history.append({
            "time": pd.Timestamp.now().strftime("%H:%M:%S"),
            "status": result["status"],
            "confidence": result["threat_probability_score"],
            "packet_size": payload["packet_size"]
        })
        
        if result["status"] == "THREAT DETECTED":
            st.session_state.threats_blocked += 1
            st.session_state.alerts.insert(0, f"🚨 Threat Blocked ({true_label} Pattern) | Confidence: {result['threat_probability_score']}% | Action: {result['recommended_action']}")
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Please ensure `python app.py` is running in another terminal.")
        st.session_state.is_running = False

    update_ui()
    time.sleep(1.5) # Wait 1.5 seconds between pings
    st.rerun() # Refresh the UI loop
else:
    update_ui() # Just draw the UI in a paused state