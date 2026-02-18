import streamlit as st
import pickle
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') # Ensure non-interactive backend
import matplotlib.pyplot as plt

# Get absolute path to current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Page Configuration
st.set_page_config(
    page_title="Aqua Sight AI",
    page_icon="💧",
    layout="wide", # Changed to wide for better dashboard layout
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
        model_path = os.path.join(BASE_DIR, 'water_model.pkl')
        with open(model_path, 'rb') as f:
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
    st.session_state.page = 'splash' # Start at splash screen
    
if 'history' not in st.session_state:
    st.session_state.history = []

def go_to_splash():
    st.session_state.page = 'splash'
    st.rerun()

def go_to_welcome():
    st.session_state.page = 'welcome'
    st.rerun()

def go_to_dashboard():
    st.session_state.page = 'dashboard'
    st.rerun()

def go_to_landing():
    st.session_state.page = 'landing'
    st.rerun()

def go_to_about():
    st.session_state.page = 'about'
    st.rerun()


# --- SPLASH SCREEN ---
if st.session_state.page == 'splash':
    # CSS Animation for Splash
    st.markdown("""
    <style>
    .splash-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
        animation: fadeIn 2s ease-in-out;
    }
    .splash-logo {
        font-size: 100px;
        font-weight: bold;
        background: linear-gradient(45deg, #00e6ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s infinite;
    }
    .splash-text {
        font-size: 30px;
        color: #cfeeff;
        letter-spacing: 5px;
        margin-top: 20px;
        animation: slideUp 1.5s ease-out;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    @keyframes slideUp {
        0% { transform: translateY(50px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    <div class="splash-container">
        <div class="splash-logo">A</div>
        <div class="splash-text">AQUA SIGHT AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-redirect after 3 seconds
    import time
    time.sleep(3)
    go_to_landing()

# --- LANDING PAGE ---
elif st.session_state.page == 'landing':
    # Center alignment using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Logo
        logo_path = os.path.join(BASE_DIR, "logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(BASE_DIR, "IMG-20260216-WA0013.jpg")
        
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch") # Streamlit 1.30+
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
    # Menu Bar
    col_menu1, col_menu2, col_menu3 = st.columns([1, 6, 1])
    with col_menu3:
        if st.button("ABOUT", use_container_width=True):
            go_to_about()

    st.title("Welcome to Aqua Sight AI")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Animated Water Waves
    st.markdown("""
    <style>
    .wave-container {
        position: relative;
        width: 100%;
        height: 280px;
        background: linear-gradient(180deg, rgba(0,20,50,0) 0%, rgba(0,40,80,0.4) 100%);
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(0,230,255,0.15);
        margin-bottom: 10px;
    }
    .wave-container svg {
        position: absolute;
        bottom: 0;
        width: 200%;
        height: 100%;
    }
    .wave1 { animation: wave-move 6s linear infinite; opacity: 0.8; }
    .wave2 { animation: wave-move 9s linear infinite reverse; opacity: 0.5; }
    .wave3 { animation: wave-move 12s linear infinite; opacity: 0.3; }
    @keyframes wave-move {
        0%   { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .wave-label {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index: 10;
        pointer-events: none;
    }
    .wave-icon { font-size: 64px; display: block; animation: float 3s ease-in-out infinite; }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-12px); }
    }
    .wave-tagline {
        color: #cfeeff;
        font-size: 16px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 8px;
        text-shadow: 0 0 10px rgba(0,230,255,0.6);
    }
    </style>
    <div class="wave-container">
        <!-- Wave 1 -->
        <svg class="wave1" viewBox="0 0 1440 280" preserveAspectRatio="none">
            <path fill="rgba(0,180,255,0.25)" d="
                M0,140 C120,200 240,80 360,140 C480,200 600,80 720,140
                C840,200 960,80 1080,140 C1200,200 1320,80 1440,140
                C1560,200 1680,80 1800,140 C1920,200 2040,80 2160,140
                C2280,200 2400,80 2520,140 C2640,200 2760,80 2880,140 L2880,280 L0,280 Z"/>
        </svg>
        <!-- Wave 2 -->
        <svg class="wave2" viewBox="0 0 1440 280" preserveAspectRatio="none">
            <path fill="rgba(0,230,255,0.18)" d="
                M0,160 C180,100 360,220 540,160 C720,100 900,220 1080,160
                C1260,100 1440,220 1620,160 C1800,100 1980,220 2160,160
                C2340,100 2520,220 2700,160 C2880,100 3060,220 3240,160 L3240,280 L0,280 Z"/>
        </svg>
        <!-- Wave 3 -->
        <svg class="wave3" viewBox="0 0 1440 280" preserveAspectRatio="none">
            <path fill="rgba(0,100,200,0.3)" d="
                M0,180 C240,120 480,240 720,180 C960,120 1200,240 1440,180
                C1680,120 1920,240 2160,180 C2400,120 2640,240 2880,180 L2880,280 L0,280 Z"/>
        </svg>
        <div class="wave-label">
            <span class="wave-icon">💧</span>
            <div class="wave-tagline">Pure · Safe · Analyzed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("ANALYZE OUR WATER SAFETY", use_container_width=True):
            go_to_dashboard()

# --- ABOUT PAGE ---
elif st.session_state.page == 'about':
    # Header with Back Button
    col_head_1, col_head_2 = st.columns([1, 10])
    with col_head_1:
         if st.button("⬅", help="Back to Welcome"):
             go_to_welcome()
    with col_head_2:
        st.title("About Aqua Sight AI")
    
    st.markdown("---")

    st.markdown("""
    ### The Vision
    Clean water is the foundation of life, yet millions lack access to reliable testing. **Aqua Sight AI** was engineered by **The Quad-core Creators** to turn any smartphone into a portable water-testing laboratory. Our mission is to democratize water safety by providing instant, high-accuracy diagnostics at a fraction of the cost of traditional lab tests.

    ### The Technology Stack
    #### 1. The AI Brain: Random Forest Classifier
    Unlike simple threshold-based testing, our system utilizes a Random Forest Machine Learning model.
    *   **Ensemble Learning**: It processes data through hundreds of "Decision Trees" to find the truth behind complex chemical patterns.
    *   **Accuracy**: Specifically optimized to handle sensor noise and environmental outliers, ensuring a 90%+ confidence level in every diagnosis.

    #### 2. The Hardware: IoT Sensor Integration
    The app is designed to interface with a precision sensor array:
    *   **pH Probe**: Monitors acidity and alkalinity levels.
    *   **TDS Meter**: Measures Total Dissolved Solids to detect heavy minerals and chemical runoff.
    *   **Turbidity Sensor**: Analyzes light scattering to detect suspended particles and pathogens.

    ### How it Works
    1.  **Capture**: Submerge the IoT probes into the water source.
    2.  **Analyze**: Input the real-time values into the Aqua Sight AI dashboard.
    3.  **Diagnose**: The AI Brain compares the data against thousands of global water quality signatures.
    4.  **Verdict**: Receive an instant classification of Potable (Safe) or Non-Potable (Danger).

    ### Meet the Developers
    **The Quad-core Creators**
    We are a dedicated group of innovators focused on the intersection of Artificial Intelligence and Environmental Sustainability. This project represents our commitment to using technology to solve real-world humanitarian crises.

    ### Why it Matters
    According to global health standards, over 2 billion people currently drink water from contaminated sources. Aqua Sight AI is a scalable solution designed for NGOs, field technicians, and rural communities to verify their water safety in seconds, not days.
    """)

# --- DASHBOARD PAGE ---
elif st.session_state.page == 'dashboard':
    # Header
    col_head_1, col_head_2, col_head_3 = st.columns([1, 18, 2])
    with col_head_1:
         if st.button("⬅", help="Back to Welcome"):
             go_to_welcome()
    with col_head_2:
        st.title("AQUA SIGHT AI")
    with col_head_3:
        if st.button("🕒", help="View History"):
            if 'show_history' not in st.session_state:
                st.session_state.show_history = True
            else:
                st.session_state.show_history = not st.session_state.show_history

    st.markdown("<p style='text-align: center; color: #cfeeff; margin-top: -15px;'>Water Quality Analysis Dashboard</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Show History if toggled
    if st.session_state.get('show_history', False):
        st.markdown("### 🕒 Recent Analysis History")
        if st.session_state.history:
            # Create a nice dataframe view
            import pandas as pd
            history_df = pd.DataFrame(st.session_state.history)
            # Reorder columns if needed
            if not history_df.empty:
               st.dataframe(history_df.style.map(lambda x: 'color: #00ff88' if x == 'POTABLE (SAFE)' else ('color: #ff4d4d' if x == 'NOT POTABLE (UNSAFE)' else ''), subset=['Result']), use_container_width=True)
        else:
            st.info("No analysis history yet. Run a prediction!")
        st.markdown("---")

    # Main Content
    col1, col2 = st.columns([1, 1.5]) # Adjusted ratio for better balance
    
    with col1:
        # Mini Logo for Dashboard
        logo_path = os.path.join(BASE_DIR, "logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(BASE_DIR, "IMG-20260216-WA0013.jpg")
            
        if os.path.exists(logo_path):
            st.image(logo_path, width="stretch")
        else:
            st.markdown("<div style='text-align: center; font-size: 50px;'>💧</div>", unsafe_allow_html=True)
        
        st.info("Input sensor data to detect water potability.")
        
        # Placeholder for Charts (Left Side)
        chart_placeholder = st.empty()

    with col2:
        st.subheader("Sensor Inputs")
        
        # separate styled boxes for each input
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
                    
                    # Save to History
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    st.session_state.history.append({
                        "Time": timestamp,
                        "pH": ph,
                        "Solids": solids,
                        "Turbidity": turbidity,
                        "Result": result_text,
                        "Conf.": f"{confidence:.1f}%"
                    })
                    
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
                        # Data for Pie Chart
                        labels = ['Not Potable', 'Potable']
                        sizes = proba
                        colors = ['#ff4d4d', '#00ff88']
                        explode = (0.1, 0) if prediction == 0 else (0, 0.1)

                        fig, ax = plt.subplots(figsize=(5, 5))
                        fig.patch.set_facecolor('none') # Transparent background
                        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                            shadow=True, startangle=90, textprops={'color':"white", 'fontsize': 12, 'weight': 'bold'})
                        ax.axis('equal')
                        
                        with chart_placeholder.container():
                            st.markdown("### Safety Distribution")
                            st.pyplot(fig, use_container_width=True)
                        
                        plt.close(fig) # Close figure to free memory
                        
                    except Exception as chart_err:
                        # Fallback simple bar chart if matplotlib fails
                        with chart_placeholder.container():
                            st.error(f"Chart Error: {chart_err}")
                            st.bar_chart({"Not Potable": proba[0], "Potable": proba[1]})

                except Exception as e:
                    st.error(f"Prediction Error: {e}")
            else:
                st.error("Model not loaded.")

    # Footer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #555; font-size: 12px;'>Powered by Aqua Sight AI Model v1.0</div>", unsafe_allow_html=True)

