import streamlit as st

def apply_theme():
    """Apply custom CSS theme with proper dark/light mode"""
    st.markdown("""
    <style>
    /* Light Theme (Default) */
    :root {
        --background-color: #ffffff;
        --text-color: #000000;
        --card-bg: #f8f9fa;
        --sidebar-bg: #f0f2f6;
        --primary-color: #4CAF50;
        --secondary-color: #2196F3;
    }
    
    /* Dark Theme */
    [data-theme="dark"] {
        --background-color: #0e1117;
        --text-color: #fafafa;
        --card-bg: #262730;
        --sidebar-bg: #1a1a1a;
        --primary-color: #4CAF50;
        --secondary-color: #2196F3;
    }
    
    /* Apply themes */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .main .block-container {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Cards */
    .card {
        background-color: var(--card-bg);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--text-color) !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color) !important;
    }
    
    /* Text */
    p, div, span {
        color: var(--text-color) !important;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    /* Select boxes, inputs */
    .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
        color: var(--text-color) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    /* Success, Info, Warning messages */
    .stAlert {
        background-color: var(--card-bg) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def set_dark_theme():
    """Set dark theme"""
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .main .block-container {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    
    .card {
        background-color: #262730;
        color: #fafafa;
        border: 1px solid #444;
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #fafafa !important;
    }
    </style>
    """, unsafe_allow_html=True)

def set_light_theme():
    """Set light theme"""
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    .main .block-container {
        background-color: #ffffff;
        color: #000000;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    
    .card {
        background-color: #f8f9fa;
        color: #000000;
        border: 1px solid #e0e0e0;
    }
    
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)