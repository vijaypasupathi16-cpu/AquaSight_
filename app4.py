import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import requests
import pickle
import importlib.util
import warnings
try:
    from sklearn.exceptions import InconsistentVersionWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
except Exception:
    pass
from sklearn.ensemble import RandomForestClassifier

# Dynamically import `st_lottie` if available, otherwise use a no-op fallback.
_spec = importlib.util.find_spec("streamlit_lottie")
if _spec is not None:
    _mod = importlib.import_module("streamlit_lottie")
    st_lottie = getattr(_mod, "st_lottie", lambda *a, **k: None)
else:
    def st_lottie(*args, **kwargs):
        return None

# --- App configuration ---
st.set_page_config(
    page_title="AquaAI | Water Quality Intelligence",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Global Background and Text */
   .stApp {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .splash-title { font-size: 4rem; font-weight: 800; text-align: center; margin-top: -50px; text-shadow: 2px 4px 10px rgba(0,0,0,0.2); }
    .splash-slogan { font-size: 1.5rem; text-align: center; font-weight: 300; opacity: 0.9; margin-bottom: 2rem; }
    div.stButton > button { display: block; margin: 0 auto; background-color: #ffffff; color: #0072ff; border-radius: 50px; padding: 0.75rem 3rem; font-size: 1.2rem; font-weight: 700; border: none; box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: all 0.3s ease-in-out; }
    div.stButton > button:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.2); color: #0056b3; background-color: #f8f9fa; }
   .dashboard-header { background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); margin-bottom: 25px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
   .team-footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: transparent; color: white; text-align: center; padding: 15px; font-size: 0.9rem; font-weight: 400; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

@st.cache_resource
def load_model_from_file(path='water_model.pkl'):
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
    except Exception:
        return None

@st.cache_resource
def make_fallback_model():
    X_sample = np.random.rand(100, 3) * np.array([14.0, 10.0, 35.0])
    y_sample = ((X_sample[:, 0] > 6.5) & (X_sample[:, 0] < 8.5) & (X_sample[:, 1] < 5.0)).astype(int)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_sample, y_sample)
    return rf

@st.cache_resource
def get_model():
    m = load_model_from_file('water_model.pkl')
    if m is None:
        return make_fallback_model()
    return m

# Initialize
apply_custom_styles()
model = get_model()
lottie_water = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'splash'

if st.session_state.current_page == 'splash':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if lottie_water:
        st_lottie(lottie_water, height=250, key="splash_lottie")
    st.markdown("<div class='splash-title'>AquaAI</div>", unsafe_allow_html=True)
    st.markdown("<div class='splash-slogan'>Intelligence for a Sustainable Future</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GET STARTED"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

elif st.session_state.current_page == 'dashboard':
    st.markdown("## 📊 Water Quality Analysis Dashboard")
    with st.container():
        st.markdown("<div class='dashboard-header'>Enter the parameters recorded by your local sensors below:</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            ph_input = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        with col2:
            turb_input = st.number_input("Turbidity (NTU)", min_value=0.0, max_value=20.0, value=3.0, step=0.1)
        with col3:
            temp_input = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.5)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("RUN AI PREDICTION"):
        with st.spinner("Analyzing spectral and chemical signatures..."):
            features = np.array([[ph_input, turb_input, temp_input]])
            try:
                prediction = model.predict(features)
            except Exception:
                st.error("Model failed to predict")
                prediction = [0]
            try:
                probs = model.predict_proba(features)
                conf = float(probs.max())
            except Exception:
                conf = 0.0
            time.sleep(1.0)
            st.divider()
            res_col, conf_col = st.columns(2)
            if prediction[0] == 1:
                res_col.success("### STATUS: POTABLE")
                conf_col.metric("Model Confidence", f"{conf*100:.1f}%", delta="Safe")
                st.balloons()
            else:
                res_col.error("### STATUS: NON-POTABLE")
                conf_col.metric("Model Confidence", f"{conf*100:.1f}%", delta="- Danger", delta_color="inverse")

    if st.sidebar.button("Back to Splash"):
        st.session_state.current_page = 'splash'
        st.rerun()

st.markdown("""
    <div class="team-footer">
        PROJECT AquaAI | POWERED BY <b>THE QUAD-CORE CREATORS</b> | VERSION 1.0.4-STABLE
    </div>
""", unsafe_allow_html=True)
