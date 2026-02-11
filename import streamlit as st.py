import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(page_title="Aqua Sight AI", page_icon="💧", layout="centered")

# --- 1. LOAD THE AI MODEL ---
# This loads the Random Forest 'brain' you trained in Colab
@st.cache_resource
def load_model():
    try:
        with open('water_model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_model()

# --- 2. USER INTERFACE (UI) ---
st.title("💧 Aqua Sight AI")
st.markdown("### *Intelligent Water Quality Monitoring*")
st.write("Presented by **The Quad-core Creators**")
st.divider()

if model is None:
    st.error("⚠️ Error: 'water_model.pkl' not found! Please place the model file in the same folder as this script.")
else:
    # --- 3. INPUT SLIDERS (Simulating IoT Sensors) ---
    st.sidebar.header("Real-time Sensor Inputs")
    st.sidebar.info("Adjust these to simulate sensor data from the ESP32.")
    
    # We use pH, Solids (TDS), and Turbidity as our key features
    ph = st.sidebar.slider("pH Level", 0.0, 14.0, 7.0, step=0.1)
    solids = st.sidebar.slider("Total Dissolved Solids (ppm)", 0, 50000, 20000)
    turbidity = st.sidebar.slider("Turbidity (NTU)", 0.0, 10.0, 3.5, step=0.1)

    # --- 4. PREDICTION LOGIC ---
    # Create a button for the judges to click
    if st.button("Analyze Water Safety"):
        # Formatting data for the model
        input_data = np.array([[ph, solids, turbidity]])
        prediction = model.predict(input_data)
        
        st.subheader("Final Verdict:")
        if prediction[0] == 1:
            st.success("✅ **POTABLE**: The water is safe for consumption.")
            st.balloons()
        else:
            st.error("❌ **NOT POTABLE**: The water is unsafe. Contaminants detected.")

    # --- 5. TECHNICAL DETAILS FOR REVIEW ---
    with st.expander("See Technical Details"):
        st.write("""
        **Data Engineering Phase:**
        - Handled 3,276 water samples.
        - Performed Mean Imputation for missing values.
        
        **AI Model Phase:**
        - Algorithm: **Random Forest Classifier**.
        - Why: High accuracy through ensemble learning (multiple decision trees).
        """)