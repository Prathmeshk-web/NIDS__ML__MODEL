# 🛡️ Enterprise Network Intrusion Detection System (NIDS)

A real-time, cloud-integrated Network Intrusion Detection System built with a Machine Learning engine (Random Forest) and deployed via IBM Cloud Watson Machine Learning. This application acts as a secure, interactive frontend dashboard that analyzes network traffic patterns to identify and flag malicious activities, such as Denial of Service (DoS) and Probe attacks.

## ✨ Core Features

* **Dual-Mode Architecture:**
    * **Instant Simulation Mode:** Test the AI's threat-detection capabilities instantly using pre-configured, scaled packet data representing both safe web browsing and malicious attack vectors.
    * **Real Traffic Upload Mode:** Upload your own network traffic logs (in CSV format) to analyze custom network connection metrics in real-time.
* **Cloud-Powered Backend:** The machine learning computation is offloaded securely to IBM Cloud via REST API, ensuring high-speed inference without burdening the local machine.
* **Frictionless Public Access:** Built utilizing Streamlit Secrets, allowing public users to test the AI model without needing their own IBM Cloud accounts or API credentials.

---

## 🚀 Live Demo
Access the live, deployed web application here: 
**[Insert Your Streamlit Cloud URL Here]**

---

## 📊 Data Requirements for Custom Uploads

If you are using the **Real Traffic Upload Mode** (Tab 2), your uploaded `.csv` file must match the exact mathematical architecture the AI was trained on. 

The Random Forest model expects exactly **41 network features** per row, modeled after the benchmark **NSL-KDD dataset**. To successfully run a prediction, your CSV columns must represent the following data points in order:

### 1. Basic TCP/IP Features
* `duration`: Length (in seconds) of the connection
* `protocol_type`: Type of protocol (e.g., TCP, UDP, ICMP)
* `service`: Network service on the destination (e.g., HTTP, FTP)
* `flag`: Status of the connection
* `src_bytes`: Bytes sent from source to destination
* `dst_bytes`: Bytes sent from destination to source
* `land`: 1 if connection is to/from the same host/port; 0 otherwise
* `wrong_fragment`: Number of wrong fragments
* `urgent`: Number of urgent packets

### 2. Content Features (Payload Analysis)
* `hot`: Number of "hot" indicators
* `num_failed_logins`: Count of failed login attempts
* `logged_in`: 1 if successfully logged in; 0 otherwise
* `num_compromised`: Number of compromised conditions
* `root_shell`: 1 if root shell is obtained; 0 otherwise
* `su_attempted`: 1 if `su root` command attempted; 0 otherwise
* `num_root`: Number of root accesses
* `num_file_creations`: Number of file creation operations
* `num_shells`: Number of shell prompts invoked
* `num_access_files`: Number of access control file operations
* `num_outbound_cmds`: Number of outbound commands in an FTP session
* `is_host_login`: 1 if the login belongs to the host; 0 otherwise
* `is_guest_login`: 1 if the login is a guest account; 0 otherwise

### 3. Time-Based Traffic Features (Past 2 Seconds)
* `count`, `srv_count`, `serror_rate`, `srv_serror_rate`, `rerror_rate`, `srv_rerror_rate`, `same_srv_rate`, `diff_srv_rate`, `srv_diff_host_rate`

### 4. Host-Based Traffic Features (Long-Term Window)
* `dst_host_count`, `dst_host_srv_count`, `dst_host_same_srv_rate`, `dst_host_diff_srv_rate`, `dst_host_same_src_port_rate`, `dst_host_srv_diff_host_rate`, `dst_host_serror_rate`, `dst_host_srv_serror_rate`, `dst_host_rerror_rate`, `dst_host_srv_rerror_rate`

> **⚠️ CRITICAL PIPELINE NOTE:** The uploaded CSV data must be pre-processed before uploading. Categorical strings (like "TCP" or "HTTP") must be mathematically encoded, and raw numerical values must be scaled using the same `StandardScaler` applied during the model's training phase.

---

## 💻 Tech Stack
* **Frontend:** Streamlit, Pandas
* **Machine Learning:** Scikit-Learn (Random Forest Classifier)
* **Cloud Infrastructure:** IBM Watson Machine Learning, Streamlit Community Cloud
* **Language:** Python 3.12

---

## 🛠️ How to Run Locally

If you wish to clone this repository and run the dashboard on your own local hardware:

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name

# Install the required Python dependencies:

Bash
pip install -r requirements.txt

# Set up your local IBM credentials:

Create a folder named .streamlit in the root directory.

Inside that folder, create a file named secrets.toml.

# Add your credentials:

Ini, TOML
IBM_API_KEY = "your_key"
IBM_SPACE_ID = "your_space_id"
IBM_DEPLOYMENT_ID = "your_deployment_id"
Boot the server:

Bash
streamlit run app.py
