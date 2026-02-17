 
import streamlit as st
import pickle
import numpy as np
import os

# Page Configuration
st.set_page_config(
    page_title="Aqua Sight AI",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load Model
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

@st.cache_resource
def load_model():
    try:
        with open('water_model.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# Custom CSS for App6 Aesthetics
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(1200px 600px at 10% 10%, rgba(0,230,255,0.03), transparent),
                    linear-gradient(180deg, #001428, #001f4d);
        color: #e6f7ff;
    }
    
    /* Input Widgets */
    .stNumberInput, .stSlider {
        background-color: transparent !important;
    }
    .stNumberInput > div > div > input {
        color: #e6f7ff;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 230, 255, 0.2);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00e6ff !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        text-shadow: 0 0 10px rgba(0, 230, 255, 0.3);
    }
    
    /* Custom Card Style */
    .css-1r6slb0, .css-12oz5g7 {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 230, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00e6ff, #4dd6ff);
        color: #001f4d;
        font-weight: bold;
        border: None;
        padding: 10px 20px;
        font-size: 18px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px rgba(0, 230, 255, 0.6);
        transform: translateY(-2px);
        color: #000;
    }

    /* Result Box */
    .result-box {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
        border: 1px solid rgba(0, 230, 255, 0.2);
    }
    .safe { color: #00ff88; font-size: 24px; font-weight: bold; }
    .unsafe { color: #ff4d4d; font-size: 24px; font-weight: bold; }
    
    /* Hide Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# SVG Waves Background (Fixed Position)
st.markdown("""
<div style="position:fixed;left:0;right:0;bottom:0;height:20vh;z-index:0;pointer-events:none;opacity:0.6;">
    <svg viewBox="0 0 1200 200" preserveAspectRatio="none" style="width:100%;height:100%;">
        <path fill="rgba(0,230,255,0.1)" d="M0,120 C150,200 350,40 600,100 C850,160 1050,40 1200,90 L1200,200 L0,200 Z"></path>
        <path fill="rgba(0,180,255,0.08)" d="M0,140 C180,80 360,200 600,150 C840,100 1020,220 1200,140 L1200,200 L0,200 Z"></path>
    </svg>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def go_to_welcome():
    st.session_state.page = 'welcome'
    st.rerun()

def go_to_dashboard():
    st.session_state.page = 'dashboard'
    st.rerun()

def go_to_landing():
    st.session_state.page = 'landing'
    st.rerun()

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    # Center alignment using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Logo
        logo_path = "logo.png"
        if not os.path.exists(logo_path):
            logo_path = "IMG-20260216-WA0013.jpg"
        
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch")
        else:
            st.markdown("<div style='text-align: center; font-size: 80px;'>💧</div>", unsafe_allow_html=True)
            
        st.markdown("""
        <h1 style='font-size: 60px; margin-bottom: 0;'>AQUA SIGHT AI</h1>
        <p style='text-align: center; color: #cfeeff; letter-spacing: 2px; text-transform: uppercase;'>Water Quality Analysis</p>
        <br>
        """, unsafe_allow_html=True)
        
        if st.button("GET STARTED", use_container_width=True):
            go_to_welcome()

# --- WELCOME PAGE ---
elif st.session_state.page == 'welcome':
    st.title("Welcome to Aqua Sight AI")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display Image (image.png or fallback)
    img_path = "image.png"
    if os.path.exists(img_path):
        st.image(img_path, width="stretch")
    else:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 50px; text-align: center; border-radius: 15px; border: 1px solid rgba(0,230,255,0.2);">
            <div style="font-size: 60px;">🌊</div>
            <p>Water Safety Visualization</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ANALYZE OUR WATER SAFETY", use_container_width=True):
            go_to_dashboard()

# --- DASHBOARD PAGE ---
elif st.session_state.page == 'dashboard':
    # Header
    col_head_1, col_head_2 = st.columns([1, 8])
    with col_head_1:
         if st.button("⬅", help="Back to Welcome"):
             go_to_welcome()
    with col_head_2:
        st.title("AQUA SIGHT AI")
    
    st.markdown("<p style='text-align: center; color: #cfeeff; margin-top: -15px;'>Water Quality Analysis Dashboard</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Main Content
    col1, col2 = st.columns([1, 1.5]) # Adjusted ratio for better balance
    
    import os
    with col1:
        # Mini Logo for Dashboard
        logo_path = "logo.png"
        if not os.path.exists(logo_path):
            logo_path = "IMG-20260216-WA0013.jpg"
            
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch")
        else:
            st.markdown("<div style='text-align: center; font-size: 50px;'>💧</div>", unsafe_allow_html=True)
        
        st.info("Input sensor data to detect water potability.")
        
        # Placeholder for Charts (Left Side)
        chart_placeholder = st.empty()

    with col2:
        st.subheader("Sensor Inputs")
        
        # Separate styled boxes for each input
        with st.container(border=True):
            ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1, help="Range: 0 - 14")
        
        with st.container(border=True):
            solids = st.number_input("Total Dissolved Solids (ppm)", min_value=0, value=20000, step=100, help="Measured in ppm")
            
        with st.container(border=True):
            turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=4.0, step=0.1, help="Lower is better")
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("RUN AI PREDICTION", use_container_width=True):
            if model:
                # Custom Water Drop Loader
                st.markdown("""
                <style>
                .loader-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100px;
                    flex-direction: column;
                }
                .drop {
                    width: 20px;
                    height: 20px;
                    background: #00e6ff;
                    border-radius: 50%;
                    position: relative;
                    animation: drop 1.5s infinite ease-in;
                }
                .drop:before {
                    content: "";
                    position: absolute;
                    top: -10px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 0;
                    height: 0;
                    border-left: 10px solid transparent;
                    border-right: 10px solid transparent;
                    border-bottom: 15px solid #00e6ff;
                }
                @keyframes drop {
                    0% { top: 0px; opacity: 1; transform: scaleX(1); }
                    80% { top: 50px; opacity: 1; transform: scaleX(0.8); }
                    100% { top: 60px; opacity: 0; transform: scaleX(0.6); }
                }
                .ripple {
                    width: 40px;
                    height: 10px;
                    border: 1px solid #00e6ff;
                    border-radius: 50%;
                    opacity: 0;
                    animation: ripple 1.5s infinite ease-out;
                    animation-delay: 1.2s;
                }
                @keyframes ripple {
                    0% { transform: scale(0.5); opacity: 1; }
                    100% { transform: scale(1.5); opacity: 0; }
                }
                </style>
                <div class="loader-container">
                    <div class="drop"></div>
                    <div class="ripple"></div>
                    <div style="color: #cfeeff; margin-top: 20px;">Analyzing Sample...</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Simulate processing time
                import time
                time.sleep(3)
                
                features = np.array([[ph, solids, turbidity]])
                
                try:
                    prediction = model.predict(features)[0]
                    proba = model.predict_proba(features)[0]
                    confidence = np.max(proba) * 100
                    
                    result_text = "POTABLE (SAFE)" if prediction == 1 else "NOT POTABLE (UNSAFE)"
                    result_class = "safe" if prediction == 1 else "unsafe"
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <div style="font-size: 14px; color: #bfefff;">ANALYSIS RESULT</div>
                        <div class="{result_class}">{result_text}</div>
                        <div style="margin-top: 10px; font-size: 12px; color: #aaa;">Confidence: {confidence:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if prediction == 1:
                        st.balloons()
                        
                    # Pie Chart Visualization in Left Column (chart_placeholder)
                    try:
                        import matplotlib.pyplot as plt
                        
                        # Data for Pie Chart
                        labels = ['Not Potable', 'Potable']
                        sizes = proba
                        colors = ['#ff4d4d', '#00ff88']
                        explode = (0.1, 0) if prediction == 0 else (0, 0.1)

                        fig, ax = plt.subplots(figsize=(4, 4))
                        fig.patch.set_facecolor('none') # Transparent background
                        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                            shadow=True, startangle=90, textprops={'color':"white", 'fontsize': 10})
                        ax.axis('equal')
                        
                        with chart_placeholder.container():
                            st.markdown("### Safety Distribution")
                            st.pyplot(fig, use_container_width=True)
                        
                    except Exception as chart_err:
                        st.error(f"Could not load chart: {chart_err}")

                except Exception as e:
                    st.error(f"Prediction Error: {e}")
            else:
                st.error("Model not loaded.")

    # Footer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #555; font-size: 12px;'>Powered by Aqua Sight AI Model v1.0</div>", unsafe_allow_html=True)
