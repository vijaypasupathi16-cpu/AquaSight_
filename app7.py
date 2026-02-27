import streamlit as st
import pickle
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') # Ensure non-interactive backend
import matplotlib.pyplot as plt
import google.generativeai as genai

# Configure Gemini (Add your API key here, or ensure it's in your environment variables before running)
# genai.configure(api_key="YOUR_API_KEY") # You can optionally uncomment and set this if you want to hardcode it

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

# --- THEME MANAGEMENT ---
# Determine current theme colors based on state (must be done before CSS injection)
# Default is Dark Mode
theme_is_dark = st.session_state.get('is_dark_mode', True)

if theme_is_dark:
    # DARK MODE COLORS
    bg_gradient = "radial-gradient(1200px 600px at 10% 10%, rgba(0,230,255,0.03), transparent), linear-gradient(180deg, #001428, #001f4d)"
    text_color = "#e6f7ff"
    header_color = "#00e6ff"
    header_shadow = "0 0 10px rgba(0, 230, 255, 0.3)"
    input_bg = "rgba(255, 255, 255, 0.05)"
    input_border = "rgba(0, 230, 255, 0.2)"
    card_bg = "rgba(255, 255, 255, 0.05)"
    btn_text_color = "#001f4d"
    btn_bg = "linear-gradient(90deg, #00e6ff, #4dd6ff)"
    label_color = "#e6f7ff"
    
    # Settings Panel Colors
    settings_bg = "rgba(0, 20, 40, 0.8)"
    settings_border = "#00e6ff"
else:
    # LIGHT MODE COLORS
    bg_gradient = "linear-gradient(180deg, #FFFFFF, #4B9CD3)" # Carolina Blue Gradient
    text_color = "#13294B" # UNC Navy Blue
    header_color = "#13294B" # UNC Navy headers
    header_shadow = "none" # Clean text for light mode
    input_bg = "rgba(255, 255, 255, 0.5)"
    input_border = "rgba(19, 41, 75, 0.4)"
    card_bg = "rgba(255, 255, 255, 0.9)"
    btn_text_color = "#13294B"
    btn_bg = "linear-gradient(90deg, #87CEFA, #4B9CD3)" # Light Blue Gradient
    label_color = "#000000" # Black labels for inputs
    
    # Settings Panel Colors
    settings_bg = "rgba(135, 206, 250, 0.6)" # Light Blue
    settings_border = "#4B9CD3"

# Custom CSS for App Aesthetics
st.markdown(f"""
<style>
    /* Main Background */
    .stApp {{
        background: {bg_gradient};
        color: {text_color};
    }}
    
    /* Input Widgets */
    .stNumberInput, .stSlider {{
        background-color: transparent !important;
    }}
    .stNumberInput > div > div > input {{
        color: {text_color};
        background-color: {input_bg};
        border: 1px solid {input_border};
    }}
    /* Input Labels (pH, Solides, etc.) */
    .stNumberInput label p, .stRadio label p, .stToggle label p {{
        color: {label_color} !important;
        font-weight: bold;
        font-size: 16px;
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: {header_color} !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        text-shadow: {header_shadow};
    }}
    
    /* Custom Card Style */
    .css-1r6slb0, .css-12oz5g7 {{
        background: {card_bg};
        border: 1px solid {input_border};
        padding: 20px;
        border-radius: 15px;
    }}
    
    /* Buttons */
    .stButton > button {{
        width: 100%;
        background: {btn_bg};
        color: {btn_text_color};
        font-weight: bold;
        border: None;
        padding: 10px 20px;
        font-size: 18px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 15px rgba(0, 230, 255, 0.6);
        transform: translateY(-2px);
        color: #000;
    }}

    /* Result Box */
    .result-box {{
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
        border: 1px solid rgba(0, 230, 255, 0.2);
    }}
    .safe {{ color: #00ff88; font-size: 24px; font-weight: bold; }}
    .unsafe {{ color: #ff4d4d; font-size: 24px; font-weight: bold; }}
    
    /* Hide Default Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
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

if 'saved_voice_style' not in st.session_state:
    st.session_state.saved_voice_style = "Female Melody"

if 'is_dark_mode' not in st.session_state:
    st.session_state.is_dark_mode = True

if 'enable_notifications' not in st.session_state:
    st.session_state.enable_notifications = True

if 'use_live_data' not in st.session_state:
    st.session_state.use_live_data = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I am your Health Advisor. Run a water analysis to get started."}]

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

def generate_health_advice(ph, tds, turbidity):
    advice = "⚠️ **Water Quality Alert!**\n\nThe AI predicted this water is **UNSAFE**. Here are the specific risks and potential side effects of drinking it:\n\n"
    has_issues = False
    
    if ph < 6.5:
        advice += "- **Low pH (Acidic):** Corrodes pipes and leaches heavy metals (like lead and copper) into the water.\n  *Side Effects if consumed:* Gastrointestinal distress, metallic taste, and long-term risk of heavy metal poisoning leading to organ damage.\n  *Medical Precaution:* If consumed, drink plenty of safe water to dilute it. If you suspect heavy metal ingestion over a long period, consult a doctor immediately for a blood test.\n"
        has_issues = True
    elif ph > 8.5:
        advice += "- **High pH (Alkaline):** Reduces the effectiveness of chlorine, allowing bacteria to survive.\n  *Side Effects if consumed:* Skin and eye irritation, bitter taste, and potential alkalosis which can cause nausea, vomiting, and muscle twitching.\n  *Medical Precaution:* If ingested, avoid antacids and drink neutral water to help balance pH levels. Seek medical help if severe nausea persists.\n"
        has_issues = True
        
    if tds > 150:
        advice += "- **High TDS:** Indicates elevated levels of dissolved minerals, salts, or potential chemical runoff.\n  *Side Effects if consumed:* Dehydration, salty or brackish taste, kidney stones, and potential exposure to toxic minerals like arsenic or nitrates.\n  *Medical Precaution:* If you experience severe cramping or signs of kidney distress, immediately seek emergency medical attention.\n"
        has_issues = True
    elif tds < 50:
         advice += "- **Very Low TDS:** Demineralized water.\n  *Side Effects if consumed:* Can leach minerals from your own body (like calcium) over time, and might cause intestinal issues due to lack of essential dietary minerals.\n  *Medical Precaution:* Short-term consumption is okay, but long-term consumption requires an adjusted diet with higher mineral intake.\n"
         has_issues = True
         
    if turbidity > 5.0:
        advice += "- **High Turbidity (Cloudy):** Suspended particles provide hiding places for harmful pathogens, viruses, and bacteria.\n  *Side Effects if consumed:* High risk of waterborne illnesses such as cholera, dysentery, diarrhea, cramps, and nausea.\n  *Medical Precaution:* If consumed, monitor for symptoms like severe diarrhea or vomiting. Take an oral rehydration solution (ORS) to prevent dehydration and visit a hospital immediately if symptoms appear.\n"
        has_issues = True
        
    if not has_issues:
         advice += "- The overall combination of these factors creates a hazardous pattern recognized by the AI, even if individual values seem marginal.\n  *Side Effects if consumed:* Unpredictable health risks ranging from mild stomach ache to serious infections depending on the exact contaminants present.\n  *Medical Precaution:* Monitor for any acute symptoms like stomach pain or fever, and consult a doctor if you feel unwell.\n"
         
    advice += "\n**Recommendation:** Do NOT consume this water. Consider advanced filtration (like Reverse Osmosis or UV light) or boiling before any use."
    return advice


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
        if st.button("SETTINGS", use_container_width=True):
            if 'show_settings' not in st.session_state:
                st.session_state.show_settings = True
            else:
                st.session_state.show_settings = not st.session_state.show_settings

    # Settings Panel
    if st.session_state.get('show_settings', False):
        st.markdown(f"""
        <div style="background: {settings_bg}; padding: 20px; border-radius: 10px; border: 1px solid {settings_border}; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">Settings</h3>
            <p>Customize your experience.</p>
        </div>
        """, unsafe_allow_html=True)
        

        with st.container():
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                # Notifications Toggle
                enable_notif = st.toggle("Enable Notifications", value=st.session_state.enable_notifications, key="notif_toggle")
                if enable_notif != st.session_state.enable_notifications:
                    st.session_state.enable_notifications = enable_notif
                
                # Voice Style Selector (Persistent)
                voice_options = ["Female Melody", "Male", "System Default"]
                try:
                    current_index = voice_options.index(st.session_state.saved_voice_style)
                except ValueError:
                    current_index = 0
                    
                selected_voice = st.radio(
                    "Voice Style", 
                    voice_options, 
                    index=current_index,
                    key="voice_style_widget", # Unique key for widget
                    help="Choose the voice for feedback."
                )
                # Save selection to persistent state
                st.session_state.saved_voice_style = selected_voice
                
            with s_col2:
                is_dark = st.toggle("Dark Mode", value=st.session_state.is_dark_mode, key="dm_toggle", help="Toggle dark or light theme.")
                # Update persistent state
                if is_dark != st.session_state.is_dark_mode:
                    st.session_state.is_dark_mode = is_dark
                    st.rerun() # Rerun to apply new CSS
                if st.button("Clear History", type="primary"):
                    st.session_state.history = []
                    st.success("History Cleared!")
                
                st.markdown("---")
                # Live Data Toggle (Moved to settings)
                live_data_toggle = st.toggle("📡 Connect Live ESP32 Wi-Fi Sensors", value=st.session_state.use_live_data, help="Connect to local API server to fetch real-time sensor variables.")
                if live_data_toggle != st.session_state.use_live_data:
                    st.session_state.use_live_data = live_data_toggle

        st.markdown("---")
        
        # Help & About Section (Inside Settings)
        with st.expander("📘 How to Perform a Test"):
            st.markdown("""
            **Step 1: Calibration.** Ensure your physical sensors (pH, TDS, and Turbidity) are calibrated and submerged in the water sample.
            
            **Step 2: Data Entry.** Observe the readings on your hardware monitor and enter those exact values into the AI Dashboard sliders or input boxes.
            
            **Step 3: Execution.** Click the "Run AI Prediction" button. The system will process these values through our Random Forest model.
            
            **Step 4: Interpretation.** Review the Safety Status and the Confidence Score to determine if the water is potable.
            """)
            
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **AI shows "Moderate" or "Unsafe":** Even if one value is "Good," the AI looks at the combination. For example, high TDS + neutral pH might still indicate chemical contamination.
            
            **Confidence is Low:** If the confidence score is below 70%, it means the data provided is near the "borderline" of safety. We recommend a second test.
            
            **Sensor Errors:** If your physical sensor shows 0 or NaN, check the wiring on your microcontroller.
            """)
            
        if st.button("ℹ️ About Aqua Sight", use_container_width=True):
            go_to_about()
            
        st.markdown("---")

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
    
    # SIDEBAR: Health Advisor Chatbot
    with st.sidebar:
        st.markdown("## 🩺 Health Advisor Chatbot")
        
        # User API Key Input
        api_key_input = st.text_input("Gemini API Key", type="password", help="Required for advanced AI chat. You can get a free one from Google AI Studio.")
        if api_key_input:
            st.session_state.gemini_api_key = api_key_input
            
        st.markdown("---")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat input
        if prompt := st.chat_input("Ask about water health..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Generative AI response logic
            try:
                # Add context to the prompt
                context_prompt = f"You are a helpful, concise Medical and Environmental Health Advisor chatbot for the 'Aqua Sight AI' water quality app. A user asks: '{prompt}'. Provide a brief, helpful, and highly accurate answer. Focus strictly on topics related to water potability, pH, TDS, Turbidity, diseases from water, and water filtration."
                
                # Check if gemini is configured (either by env var or code)
                if st.session_state.get('gemini_api_key'):
                     genai.configure(api_key=st.session_state.gemini_api_key)
                     gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')
                     bot_response = gemini_model.generate_content(context_prompt)
                     response = bot_response.text
                else:
                     response = "⚠️ Please enter your Gemini API Key in the sidebar above to enable advanced AI chat! You can get a free one from [Google AI Studio](https://aistudio.google.com/)."
            except Exception as e:
                # Fallback if API fails or no key
                response = f"I am unable to reach my AI brain at the moment (Error: {e}). Please check your API key and connection."
                
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

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
        
        # Default Variables Set
        import json
        
        default_ph = 7.0
        default_tds = 100
        default_turbidity = 4.0
        
        if st.session_state.use_live_data:
            data_file = os.path.join(BASE_DIR, 'sensor_data.json')
            if os.path.exists(data_file):
                try:
                    with open(data_file, 'r') as f:
                        live_data = json.load(f)
                    # Use values from JSON, fallback to defaults if keys are missing
                    default_ph = float(live_data.get('ph', 7.0))
                    default_tds = int(live_data.get('tds', 100))
                    default_turbidity = float(live_data.get('turbidity', 4.0))
                    st.success("✅ Connected: Reading live values from ESP32 API.", icon="📡")
                except Exception as e:
                    st.error(f"Error reading live data file: {e}")
            else:
                st.warning("⏳ Waiting for ESP32 data... Please start `sensor_api.py` and power on your ESP32.")
        
        # separate styled boxes for each input
        with st.container(border=True):
            ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=default_ph, step=0.1, help="Range: 0 - 14", disabled=st.session_state.use_live_data)
        
        with st.container(border=True):
            solids = int(st.number_input("Total Dissolved Solids (ppm)", min_value=0, value=default_tds, step=10, help="Measured in ppm", disabled=st.session_state.use_live_data))
            
        with st.container(border=True):
            turbidity = st.number_input("Turbidity (NTU)", min_value=0.0, value=default_turbidity, step=0.1, help="Lower is better", disabled=st.session_state.use_live_data)
        
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
                    if not (6.5 <= ph <= 8.5) or not (50 <= solids <= 150) or not (0.0 <= turbidity <= 5.0):
                        prediction = 0
                        proba = np.array([1.0, 0.0])
                        confidence = 100.0
                    else:
                        prediction = model.predict(features)[0]
                        proba = model.predict_proba(features)[0]
                        confidence = np.max(proba) * 100
                    
                    result_text = "POTABLE (SAFE)" if prediction == 1 else "NOT POTABLE (UNSAFE)"
                    result_class = "safe" if prediction == 1 else "unsafe"
                    
                    # Voice Message
                    if prediction == 1:
                        voice_msg = "You can drink this! The water is safe."
                    else:
                        voice_msg = "Don't drink the water! It is not safe."
                    
                    # JavaScript for Browser TTS
                    # We use a unique key based on timestamp to ensure it re-runs if needed, 
                    # though 'html' component usually runs on render.
                    html_code = f"""
                    <script>
                        window.speechSynthesis.onvoiceschanged = function() {{
                            var voices = window.speechSynthesis.getVoices();
                            var msg = new SpeechSynthesisUtterance("{voice_msg}");
                            
                            // Get selected style from Streamlit state
                            var style = "{st.session_state.saved_voice_style}";
                            
                            if (style.includes("Female Melody")) {{
                                // FEMALE MELODY MODE
                                msg.pitch = 1.2; 
                                msg.rate = 1.0;
                                var femaleVoice = voices.find(v => v.name.includes("Zira") || v.name.includes("Female") || v.name.includes("Google US English"));
                                if (femaleVoice) {{ msg.voice = femaleVoice; }}
                                
                                window.speechSynthesis.cancel();
                                window.speechSynthesis.speak(msg);
                                
                                // Repeat for melody mode
                                var msg2 = new SpeechSynthesisUtterance("{voice_msg}");
                                if (femaleVoice) {{ msg2.voice = femaleVoice; }}
                                msg2.pitch = 1.2; msg2.rate = 1.0;
                                window.speechSynthesis.speak(msg2);
                                
                            }} else if (style.includes("Male")) {{
                                // MALE MODE (FORMERLY SHINCHAN)
                                msg.pitch = 1.6; 
                                msg.rate = 1.1;
                                var maleVoice = voices.find(v => v.name.includes("David") || v.name.includes("Male") || v.name.includes("Google US English"));
                                if (maleVoice) {{ msg.voice = maleVoice; }}
                                
                                window.speechSynthesis.cancel();
                                window.speechSynthesis.speak(msg);
                                
                            }} else {{
                                // SYSTEM DEFAULT
                                window.speechSynthesis.cancel();
                                window.speechSynthesis.speak(msg);
                            }}
                        }};
                        
                        if (window.speechSynthesis.getVoices().length > 0) {{
                            window.speechSynthesis.onvoiceschanged();
                        }}
                    </script>
                    """
                    import streamlit.components.v1 as components
                    components.html(html_code, height=0)

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
                    
                    # TRIGGER NOTIFICATION (Toast)
                    if st.session_state.enable_notifications:
                        if prediction == 1:
                            st.toast("✅ Analysis Complete: Water is Safe!", icon="💧")
                        else:
                            st.toast("⚠️ Analysis Complete: Water is Unsafe!", icon="🚫")
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <div style="font-size: 14px; color: #bfefff;">ANALYSIS RESULT</div>
                        <div class="{result_class}">{result_text}</div>
                        <div style="margin-top: 10px; font-size: 12px; color: #aaa;">Confidence: {confidence:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if prediction == 1:
                        # SAFE
                        st.balloons()
                        msg_color = "#00ff88"
                        display_msg = "You can drink this! The water is safe."
                        st.session_state.chat_history = [{"role": "assistant", "content": "✅ Great news! Your latest sample was safe. You can drink this water."}]
                    else:
                        # UNSAFE
                        msg_color = "#ff4d4d"
                        display_msg = "Don't drink the water! It is not safe."
                        advice = generate_health_advice(ph, solids, turbidity)
                        st.session_state.chat_history = [{"role": "assistant", "content": advice}]

                    # Display the Message (Standardized Box)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""
                     <div style="
                        background: rgba(255,255,255,0.05); 
                        border-left: 5px solid {msg_color}; 
                        padding: 20px; 
                        border-radius: 10px; 
                        margin-top: 10px;
                        font-size: 22px;
                        text-align: center;
                        font-weight: bold;
                        color: #cfeeff;">
                        {display_msg}
                     </div>
                     """, unsafe_allow_html=True)
                        
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

