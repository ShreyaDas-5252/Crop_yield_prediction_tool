import streamlit as st
from app.components.ui import set_theme, header, footer

def main():
    dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=False)
    set_theme(dark_mode)

    header("ℹ️ About this Project", "Crop Yield Prediction Tool — Streamlit + MySQL")

    st.markdown("""
    👨‍💻 **Authors:** Harsh Raj, Harsh Kumar, Hardik  
    👩‍🏫 **Supervisor:** Dr. Ravneet Kaur  

    🌾 This tool was built to provide farmers with a lightweight, interactive way to estimate crop yields.  
    📊 The model is trained on features such as rainfall, temperature, humidity, soil pH and fertilizer usage.
    """)
    st.markdown("📚 **References:** see project synopsis.")
    footer()

if __name__ == "__main__":
    main()
