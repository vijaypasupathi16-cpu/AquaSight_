import streamlit as st
import pandas as pd
import pickle

# 1. Load the AI Model (The Brain)
def load_model():
    with open('water_model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

# 2. Page Header
st.set_page_config(page_title="Aqua Sight AI", page_icon="💧")
st.title("💧 Aqua Sight AI")
st.subheader("Intelligent System for Real-time Water Safety")
st.write("Developed by **The Quad-core Creators**")

# 3. User Input (Simulating Sensors)
st.sidebar.header("Sensor Inputs")
ph = st.sidebar.slider("pH Level", 0.0, 14.0, 7.0)
solids = st.sidebar.slider("Total Dissolved Solids (ppm)", 0, 50000, 20000)
turbidity = st.sidebar.slider("Turbidity (NTU)", 0.0, 10.0, 3.0)

# 4. AI Prediction Logic
if st.button("Analyze Water Safety"):
    # Making a prediction using the Random Forest model
    features = [[ph, solids, turbidity]]
    prediction = model.predict(features)
    
    if prediction[0] == 1:
        st.success("✅ Verdict: Potable (Safe to Drink)")
        st.balloons()
    else:
        st.error("❌ Verdict: Not Potable (Unsafe)")

# 5. Technical Info for Judges
st.info("Model: Random Forest Classifier | Dataset: 3,276 Samples")
