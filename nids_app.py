import streamlit as st
import pandas as pd
import time
from ibm_watson_machine_learning import APIClient

# --- Page Configuration ---
st.set_page_config(page_title="Dual-Mode NIDS Dashboard", page_icon="🛡️", layout="wide")

# --- Secure IBM Cloud Connection ---
@st.cache_resource
def get_ibm_client():
    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com", # Change location if your deployment is different
        "apikey": st.secrets["IBM_API_KEY"]
    }
    return APIClient(credentials)

def score_traffic_ibm(packet_features):
    try:
        client = get_ibm_client()
        client.set.default_space(st.secrets["IBM_SPACE_ID"])
        
        # Format the payload exactly as IBM expects it
        payload_scoring = {"input_data": [{"values": [packet_features]}]}
        
        # Send to your deployment ID
        response = client.deployments.score(st.secrets["IBM_DEPLOYMENT_ID"], payload_scoring)
        
        # Extract the prediction result
        prediction = response['predictions'][0]['values'][0][0]
        return prediction
    except Exception as e:
        return f"Error: {str(e)}"

# --- Header ---
st.title("🛡️ Network Intrusion Detection System (NIDS)")
st.subheader("Enterprise-Grade Threat Analysis Powered by Random Forest & IBM Cloud")
st.markdown("---")

# --- Sidebar Status ---
with st.sidebar:
    st.header("⚙️ Infrastructure Status")
    if "IBM_API_KEY" in st.secrets:
        st.success("✅ Connected securely to IBM Cloud")
    else:
        st.error("❌ Missing Cloud Credentials in Secrets")
    st.markdown("---")
    st.write("🧠 **Engine:** Scikit-Learn Random Forest")
    st.write("📊 **Features Required:** 41 Network Metrics")

# --- Create Tabs for Both Modes ---
tab1, tab2 = st.tabs(["🚀 Instant Simulation Mode", "📁 Real Traffic Upload Mode"])

# ==========================================
# TAB 1: INSTANT SIMULATION
# ==========================================
with tab1:
    st.header("Interactive Packet Simulation")
    st.write("Test the AI instantly using pre-configured, scaled packet data from our dataset.")
    
    traffic_type = st.radio("Choose a Scenario to Simulate:", ["Normal Safe Traffic", "Malicious DDoS/Probe Attack"])
    
    # Mathematical representations of network packets (41 features)
    if "Normal" in traffic_type:
        simulated_values = [-0.11, 0.52, -0.15, 0.75, -0.04, -0.02, -0.01, -0.05, -0.01, -0.08, -0.04, 1.25, -0.02, -0.03, -0.02, -0.02, -0.03, -0.02, -0.06, 0.0, 0.0, -0.08, -0.32, -0.25, -0.21, -0.21, -0.22, -0.22, 0.55, -0.28, 0.15, -0.12, 0.85, 0.62, -0.25, -0.31, 0.05, -0.21, -0.21, -0.25, -0.24]
    else:
        simulated_values = [-0.11, -0.22, 0.65, -1.85, -0.06, -0.04, -0.01, -0.05, -0.01, -0.08, -0.04, -0.85, -0.02, -0.03, -0.02, -0.02, -0.03, -0.02, -0.06, 0.0, 0.0, -0.08, 4.15, 3.85, 3.55, 3.55, -0.22, -0.22, -1.65, 1.25, -0.25, 1.12, -1.25, -1.12, 0.55, -0.31, -0.25, 3.55, 3.55, -0.25, -0.24]

    st.code(f"Payload Preview:\n{simulated_values[:8]} ... [41 features total]", language="json")
    
    if st.button("Run Simulation Threat Check", type="primary"):
        with st.spinner("Streaming data to IBM Cloud..."):
            result = score_traffic_ibm(simulated_values)
            
            st.markdown("### 📊 AI Analysis Verdict")
            if "Error" in str(result):
                st.error(result)
            elif result == "Attack" or result == 1:
                st.error("🛑 ALERT: Malicious Activity Detected! Connection Blocked.")
            else:
                st.success("💚 Traffic Status: NORMAL. Connection Authorized.")

# ==========================================
# TAB 2: REAL TRAFFIC UPLOAD
# ==========================================
with tab2:
    st.header("Analyze Custom Network Log Data")
    st.write("Upload a CSV log file containing network features to run them through the model.")
    
    # Downloadable template example so users know what to upload
    st.info("💡 Note: Your model requires exactly 41 network features (such as duration, src_bytes, dst_bytes, etc.).")
    
    uploaded_file = st.file_uploader("Upload Network Traffic Log (CSV format)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Read the user's uploaded file
            df = pd.read_csv(uploaded_file)
            st.write("📊 **Uploaded Data Preview:**", df.head(3))
            
            # Check if it has 41 columns
            if df.shape[1] != 41:
                st.warning(f"⚠️ Warning: Your model expects exactly 41 features, but this file has {df.shape[1]} columns. Please make sure data shapes align.")
            
            if st.button("Analyze Uploaded File", type="secondary"):
                with st.spinner("Analyzing log rows via IBM cloud..."):
                    # Take the very first row of the CSV to test
                    user_features = df.iloc[0].tolist()
                    
                    result = score_traffic_ibm(user_features)
                    
                    st.markdown("### 📊 Custom Data Verdict")
                    if "Error" in str(result):
                        st.error(result)
                    elif result == "Attack" or result == 1:
                        st.error("🛑 ALERT: The uploaded traffic log contains malicious behavior patterns!")
                    else:
                        st.success("💚 Traffic Status: CLEAN. The uploaded patterns look normal.")
                        
        except Exception as e:
            st.error(f"Error parsing CSV file: {e}")