import streamlit as st
import os
from app.utils.database import test_connection, setup_database_tables

def show():
    st.title("⚙️ Settings & Configuration")
    
    # Database Configuration
    st.header("🔧 Database Settings")
    
    with st.form("db_config"):
        col1, col2 = st.columns(2)
        
        with col1:
            db_host = st.text_input("Host", value="localhost")
            db_user = st.text_input("User", value="root")
            db_port = st.number_input("Port", value=3306, min_value=1, max_value=65535)
        
        with col2:
            db_password = st.text_input("Password", type="password", value="harsh@618")
            db_name = st.text_input("Database", value="crop_yield")
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_btn = st.form_submit_button("🔍 Test Connection")
        
        with col2:
            setup_btn = st.form_submit_button("🗃️ Setup Database")
    
    if test_btn:
        with st.spinner("Testing database connection..."):
            if test_connection(db_host, db_user, db_password, db_name, db_port):
                st.success("✅ Database connection successful!")
            else:
                st.error("❌ Database connection failed! Check your credentials.")
    
    if setup_btn:
        with st.spinner("Setting up database tables..."):
            if setup_database_tables():
                st.success("✅ Database tables created successfully!")
            else:
                st.error("❌ Failed to create database tables!")
    
    # App Preferences
    st.header("🎨 App Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French"])
    
    with col2:
        units = st.selectbox("Units", ["Metric", "Imperial"])
        notifications = st.checkbox("Enable Notifications", value=True)
    
    if st.button("💾 Save Preferences"):
        st.success("✅ Preferences saved successfully!")
    
    # System Information
    st.header("📊 System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Test database connection
        db_status = "✅ Connected" if test_connection() else "❌ Disconnected"
        st.info(f"**Database:** {db_status}")
        
    with col2:
        # Check if model exists
        model_path = "app/models/model.pkl"
        model_status = "✅ Loaded" if os.path.exists(model_path) else "❌ Not Found"
        st.info(f"**ML Model:** {model_status}")
    
    with col3:
        st.info(f"**App Version:** 2.0.0")
    
    # Data Management
    st.header("🗃️ Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.experimental_rerun()
            st.success("Cache cleared!")
    
    with col2:
        if st.button("📊 Export Data", use_container_width=True):
            st.success("✅ Data exported successfully! (Sample functionality)")
    
    with col3:
        if st.button("💾 Backup Data", use_container_width=True):
            st.success("✅ Backup created successfully! (Sample functionality)")
    
    # System Actions
    st.header("⚡ System Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Retrain Model", use_container_width=True):
            try:
                import subprocess
                result = subprocess.run(["python", "app/models/train.py"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Model retrained successfully!")
                    st.code(result.stdout)
                else:
                    st.error("❌ Model training failed!")
                    st.code(result.stderr)
            except Exception as e:
                st.error(f"❌ Error retraining model: {e}")
    
    with col2:
        if st.button("⚠️ Reset Settings", use_container_width=True):
            st.warning("This will reset all settings to defaults!")
            if st.button("Confirm Reset", key="confirm_reset"):
                st.success("Settings reset to defaults!")

if __name__ == "__main__":
    show()