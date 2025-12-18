import streamlit as st
import sys
import os
from pathlib import Path

# Add path fixing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Crop Yield Pro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PERFECT AGRICULTURE THEME FUNCTIONS
def apply_theme(theme_mode="Light"):
    """Apply perfect agriculture-themed CSS for both modes"""
    if theme_mode == "Dark":
        # DARK AGRICULTURE THEME - Perfect visibility
        st.markdown("""
        <style>
        /* Dark Agriculture Theme - Perfect Contrast */
        .stApp {
            background: linear-gradient(135deg, #0a2f0a 0%, #1a472a 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main .block-container { background-color: transparent; color: #ffffff; }
        .stMarkdown, .stMarkdown p, .stMarkdown div { color: #ffffff !important; }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 100%) !important;
            border-right: 3px solid #4caf50;
        }
        section[data-testid="stSidebar"] * { color: #ffffff !important; }
        .stRadio label { color: #ffffff !important; font-weight: 600; }
        .stRadio [data-testid="stMarkdownContainer"] { color: #ffffff !important; }
        h1, h2, h3, h4, h5, h6 {
            color: #c8e6c9 !important; font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        p, div, span, li { color: #e8f5e8 !important; }
        .stDataFrame { background-color: #1b5e20 !important; color: #ffffff !important; }
        .stAlert { background-color: #2e7d32 !important; border: 2px solid #4caf50;
                   border-radius: 10px; color: #ffffff !important; }
        .agri-card {
            background: linear-gradient(135deg, #2e7d32 0%, #388e3c 100%);
            padding: 2rem; border-radius: 15px; border: 2px solid #4caf50;
            margin-bottom: 1.5rem; color: #ffffff;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }
        .agri-metric {
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white; padding: 1.5rem; border-radius: 12px; text-align: center;
            border: 2px solid #81c784; box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .stButton>button {
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white; border: none; padding: 0.7rem 1.5rem; border-radius: 8px;
            cursor: pointer; font-weight: 600; font-size: 1rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #1b5e20; color: white !important;
            border: 2px solid #4caf50; border-radius: 8px;
        }
        .stSelectbox>div>div {
            background-color: #1b5e20; color: white !important;
            border: 2px solid #4caf50; border-radius: 8px;
        }
        .stSlider>div>div>div { background-color: #4caf50; }
        .streamlit-expanderHeader {
            background-color: #2e7d32 !important; color: #ffffff !important;
            border: 2px solid #4caf50; border-radius: 8px; font-weight: 600;
        }
        .st-bw, .st-c0, .st-c1, .st-c2, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7, .st-c8, .st-c9 {
            color: #ffffff !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # LIGHT AGRICULTURE THEME
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e8 50%, #f1f8e9 100%);
            color: #1b5e20;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main .block-container { background-color: transparent; color: #1b5e20; }
        .stMarkdown, .stMarkdown p, .stMarkdown div { color: #1b5e20 !important; }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #4caf50 0%, #66bb6a 100%) !important;
            border-right: 3px solid #388e3c;
        }
        section[data-testid="stSidebar"] * { color: #ffffff !important; }
        .stRadio label { color: #ffffff !important; font-weight: 600; }
        h1, h2, h3, h4, h5, h6 { color: #1b5e20 !important; font-weight: 700; }
        h1 {
            background: linear-gradient(135deg, #2e7d32, #4caf50);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; font-weight: 800;
        }
        p, div, span, li { color: #2e7d32 !important; font-weight: 500; }
        .agri-card {
            background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
            padding: 2rem; border-radius: 15px; border: 3px solid #4caf50;
            margin-bottom: 1.5rem; color: #1b5e20;
            box-shadow: 0 8px 16px rgba(76, 175, 80, 0.2);
        }
        .agri-metric {
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white; padding: 1.5rem; border-radius: 12px; text-align: center;
            border: 2px solid #388e3c; box-shadow: 0 6px 12px rgba(76, 175, 80, 0.3);
        }
        .stButton>button {
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white; border: none; padding: 0.7rem 1.5rem; border-radius: 8px;
            cursor: pointer; font-weight: 600; font-size: 1rem;
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3); transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4);
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #ffffff; color: #1b5e20 !important;
            border: 2px solid #4caf50; border-radius: 8px; font-weight: 500;
        }
        .stSelectbox>div>div {
            background-color: #ffffff; color: #1b5e20 !important;
            border: 2px solid #4caf50; border-radius: 8px; font-weight: 500;
        }
        .stSlider>div>div>div { background-color: #4caf50; }
        .streamlit-expanderHeader {
            background-color: #e8f5e8 !important; color: #1b5e20 !important;
            border: 2px solid #4caf50; border-radius: 8px; font-weight: 600;
        }
        .st-bw, .st-c0, .st-c1, .st-c2, .st-c3, .st-c4, .st-c5, .st-c6, .st-c7, .st-c8, .st-c9 {
            color: #1b5e20 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"

# Apply initial theme
apply_theme(st.session_state.theme)

def show_fallback_home():
    """Agriculture-themed fallback home page with centered emojis."""
    
    # Main header section
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0; padding: 3rem;
    background: linear-gradient(135deg, #4caf50, #66bb6a); border-radius: 15px; color: white;'>
        <h1 style='color: white; margin: 0.5rem 0; font-size: 3.5rem;'>🌱 Crop Yield Pro</h1>
        <p style='color: #e8f5e8; font-size: 1.8rem; margin: 1rem 0; font-weight: 600;'>AI-Powered Agricultural Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    # Main content card with centered emojis
    st.markdown("""
    <div class='agri-card'>
        <h1 style='text-align: center; font-size: 2.5rem;'>Welcome to Crop Yield Pro</h1>
        <p style='text-align: center; font-size: 1.5rem; font-weight: 600; margin: 1rem 0;'>
        <strong>AI-Powered Agricultural Intelligence Platform</strong>
        </p>
        <div style='text-align: center; margin: 2rem 0;'>
            <span style='font-size: 4rem;'>🤖 🌱 📊</span>
        </div>
        <p style='text-align: center; font-size: 1.3rem; line-height: 1.6;'>
        Maximize your crop yields with data-driven insights, predictive analytics, and personalized recommendations.
        </p>
        
        <h3 style='border-bottom: 3px solid #4caf50; padding-bottom: 0.8rem; text-align: center; font-size: 1.8rem;'>Features:</h3>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 2rem;'>
            <div style='background: rgba(76, 175, 80, 0.15); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4caf50;'>
                <strong style='font-size: 1.3rem;'>🌾 Yield Prediction</strong><br>
                <span style='font-size: 1.1rem;'>Accurate crop yield forecasts</span>
            </div>
            <div style='background: rgba(76, 175, 80, 0.15); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4caf50;'>
                <strong style='font-size: 1.3rem;'>📊 Farmer Dashboard</strong><br>
                <span style='font-size: 1.1rem;'>Visual analytics and insights</span>
            </div>
            <div style='background: rgba(76, 175, 80, 0.15); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4caf50;'>
                <strong style='font-size: 1.3rem;'>📈 Farm Analytics</strong><br>
                <span style='font-size: 1.1rem;'>Economic and risk analysis</span>
            </div>
            <div style='background: rgba(76, 175, 80, 0.15); padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4caf50;'>
                <strong style='font-size: 1.3rem;'>💡 Smart Recommendations</strong><br>
                <span style='font-size: 1.1rem;'>Personalized farming advice</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Agriculture-themed metrics
    st.markdown("## 📊 Farm Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="agri-metric">', unsafe_allow_html=True)
        st.metric("Total Predictions", "1,247", "12%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="agri-metric">', unsafe_allow_html=True)
        st.metric("Yield Increase", "23%", "5%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="agri-metric">', unsafe_allow_html=True)
        st.metric("Cost Savings", "₹45,600", "8%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="agri-metric">', unsafe_allow_html=True)
        st.metric("Success Rate", "94%", "2%")
        st.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #388e3c, #4caf50); border-radius: 10px; margin-bottom: 1rem;'>
            <h1 style='color: white; margin: 0; font-size: 1.8rem;'>🌱 Crop Yield Pro</h1>
            <p style='color: #e8f5e8; margin: 0; font-size: 0.9rem;'>Smart Farming Solutions</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.write("**🎨 Theme Settings**")
        theme = st.radio(
            "Select Theme:",
            ["Light ☀️", "Dark 🌙"],
            index=0 if st.session_state.theme == "Light" else 1,
            key="theme_selector",
            label_visibility="collapsed"
        )
        theme_value = "Light" if "Light" in theme else "Dark"
        if theme_value != st.session_state.theme:
            st.session_state.theme = theme_value
            apply_theme(theme_value)
            st.rerun()

        st.markdown("---")
        st.write("**🧭 Navigation**")
        page = st.radio(
            "Go to:",
            ["🏠 Home","🌾 Predict Yield","📊 Farmer Dashboard",
             "📈 Farm Analytics","💡 Smart Recommendations","⚙️ Farm Settings"],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #388e3c, #4caf50); padding: 1rem; border-radius: 10px; color: white;'>
        <h4 style='color: white; text-align: center; margin-bottom: 0.5rem;'>🌿 Farming Tip</h4>
        <p style='text-align: center; font-size: 0.9rem; margin: 0;'>
        "Regular soil testing can increase crop yield by up to 25%"
        </p>
        </div>
        """, unsafe_allow_html=True)

    apply_theme(st.session_state.theme)
    page_name = page.split(" ", 1)[1] if " " in page else page

    if page_name == "Home":
        try:
            from app.pages.home import show
            show()
        except Exception as e:
            st.error(f"Home page error: {e}")
            show_fallback_home()
    elif page_name == "Predict Yield":
        try:
            from app.pages.predict import show
            show()
        except Exception as e:
            st.error(f"Prediction page error: {e}")
    elif page_name == "Farmer Dashboard":
        try:
            from app.pages.dashboard import show
            show()
        except Exception as e:
            st.error(f"Dashboard page error: {e}")
    elif page_name == "Farm Analytics":
        try:
            from app.pages.analytics import show
            show()
        except Exception as e:
            st.error(f"Analytics page error: {e}")
    elif page_name == "Smart Recommendations":
        try:
            from app.pages.recommendations import show
            show()
        except Exception as e:
            st.error(f"Recommendations page error: {e}")
    elif page_name == "Farm Settings":
        try:
            from app.pages.settings import show
            show()
        except Exception as e:
            st.error(f"Settings page error: {e}")

if __name__ == "__main__":
    main()