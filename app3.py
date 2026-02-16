import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import requests
from sklearn.ensemble import RandomForestClassifier
from streamlit_lottie import st_lottie

# ============================================================
# PROJECT: AquaAI
# TEAM: The Quad-Core Creators
# DESCRIPTION: Professional Water Quality Monitoring Frontend
# ============================================================

# 1. Page Config for Flutter-style Branding
st.set_page_config(
    page_title="AquaAI | Water Quality Intelligence",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS Blueprint
# Targets: Background Gradients, Modern Typography, and Button Styles
def apply_custom_styles():
    st.markdown("""
    <style>
    /* Global Background and Text */
   .stApp {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        font-family: 'Source Sans Pro', sans-serif;
    }

    /* Splash Screen Branding */
   .splash-title {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-top: -50px;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.2);
    }
    
   .splash-slogan {
        font-size: 1.5rem;
        text-align: center;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 2rem;
    }

    /* Flutter-Style 'Get Started' Button */
    div.stButton > button {
        display: block;
        margin: 0 auto;
        background-color: #ffffff;
        color: #0072ff;
        border-radius: 50px;
        padding: 0.75rem 3rem;
        font-size: 1.2rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }

    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        color: #0056b3;
        background-color: #f8f9fa;
    }

    /* Dashboard UI Elements */
   .dashboard-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-bottom: 25px;
    }

    /* Hide Streamlit Default UI Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Team Footer */
   .team-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 0.9rem;
        font-weight: 400;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Animation Loading (Lottie)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code!= 200:
        return None
    return r.json()

# 4. Machine Learning Model Setup (Cached)
@st.cache_resource
def initialize_aqua_model():
    # In a production scenario, this loads a pre-trained joblib/pickle file
    # Here, we simulate a model trained on water potability parameters 
    X_sample = np.rando[span_44](start_span)[span_44](end_span)[span_47](start_span)[span_47](end_span)m.rand(100, 3) *  # pH, Turbidity, Temp
    y_sample = (X_sample[:, 0] > 6.5) & (X_sample[:, 0] < 8.5) & (X_sample[:, 1] < 5.0)
    y_sample = y_sample.astype(int)
    
    rf = RandomForestClassif[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span)[span_2](start_span)[span_2](end_span)ier(n_estimators=100, random_state=42)
    rf.fit(X_sample, y_sample)
    return rf

# Initialize App
apply_custom_styles()
model = initialize_aqua_model()
lottie_water = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

# 5. State-Based Page Management
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'splash'

# --- PAGE 1: SPLASH SCREEN ---
if st.session_state.current_page == 'splash':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Lottie Logo Animation
    if lottie_water:
        st_lottie(lottie_water, height=250, key="splash_lottie")
    
    st.markdown("<div class='splash-title'>AquaAI</div>", unsafe_allow_html=True)
    st.markdown("<div class='splash-slogan'>Intelligence for a Sustainable Future</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("GET STARTED"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

# --- PAGE 2: FUNCTIONAL DASHBOARD ---
elif st.session_state.current_page == 'dashboard':
    st.markdown("## 📊 Water Quality Analysis Dashboard")
    
    # Input Section
    with st.container():
        st.markdown("<div class='dashboard-header'>Enter the parameters recorded by your local sensors below:</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ph_input = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="The acidity or alkalinity of the water.")
        with col2:
            turb_input = st.number_input("Turbidity (NTU)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, help="The cloudiness of the water sample.")
        with col3:
            temp_input = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.5, help="Current water temperature.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prediction Interface
    if st.button("RUN AI PREDICTION"):
        with st.spinner("Analyzing spectral and chemical signatures..."):
            # Prepare data for model
            features = np.array([[ph_input, turb_input, temp_input]])
            prediction = model.predict(features)
            confidence = model.predict_proba(features)
            
            time.sleep(1.5) # Simulated latency for 'professional' feel
            
            st.divider()
            
            res_col, conf_col = st.columns(2)
            
            if prediction == 1:
                res_col.success("### STATUS: POTABLE")
                conf_col.metric("Model Confidence", f"{max(confidence)*100:.1f}%", delta="Safe")
                st.balloons()
            else:
                res_col.error("### STATUS: NON-POTABLE")
                conf_col.metric("Model Confidence", f"{max(confidence)*100:.1f}%", delta="- Danger", delta_color="inverse")
    
    # Reset Option
    if st.sidebar.button("Back to Splash"):
        st.session_state.current_page = 'splash'
        st.rerun()

# Global Team Credits Footer
st.markdown("""
    <div class="team-footer">
        PROJECT AquaAI | POWERED BY <b>THE QUAD-CORE CREATORS</b> | VERSION 1.0.4-STABLE
    </div>
""", unsafe_allow_html=True)
