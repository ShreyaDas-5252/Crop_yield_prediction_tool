import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.markdown("""
    <div class='agri-card'>
    <h1 style='text-align: center;'>🌱 Welcome to Crop Yield Pro</h1>
    <p style='text-align: center; font-size: 1.2rem; font-weight: 500;'>
    <strong>AI-Powered Agricultural Intelligence Platform</strong>
    </p>
    
    <p style='text-align: center; font-size: 1.1rem;'>
    Maximize your crop yields with data-driven insights, 
    predictive analytics, and personalized recommendations.
    </p>
    
    <h3 style='border-bottom: 2px solid #4caf50; padding-bottom: 0.5rem;'>Features:</h3>
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
        <div style='background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;'>
            <strong>🌾 Yield Prediction</strong><br>
            Accurate crop yield forecasts
        </div>
        <div style='background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;'>
            <strong>📊 Farmer Dashboard</strong><br>
            Visual analytics and insights
        </div>
        <div style='background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;'>
            <strong>📈 Farm Analytics</strong><br>
            Economic and risk analysis
        </div>
        <div style='background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #4caf50;'>
            <strong>💡 Smart Recommendations</strong><br>
            Personalized farming advice
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
    
    # Agriculture charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="agri-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Crop Yield Trends")
        data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Wheat': [2.5, 2.8, 3.1, 2.9, 3.2, 3.5],
            'Rice': [3.2, 3.4, 3.6, 3.8, 4.0, 4.2],
            'Corn': [2.8, 3.0, 3.3, 3.5, 3.7, 4.0]
        })
        fig = px.line(data, x='Month', y=['Wheat', 'Rice', 'Corn'], 
                     title='Monthly Yield Trends (tons/hectare)',
                     color_discrete_sequence=['#4caf50', '#ff9800', '#2196f3'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="agri-card">', unsafe_allow_html=True)
        st.markdown("### 🌾 Farm Distribution")
        crop_data = pd.DataFrame({
            'Crop': ['Wheat', 'Rice', 'Corn', 'Soybean', 'Others'],
            'Area': [35, 25, 20, 15, 5]
        })
        fig = px.pie(crop_data, values='Area', names='Crop', 
                    title='Crop Distribution by Area (%)',
                    color_discrete_sequence=['#4caf50', '#66bb6a', '#81c784', '#a5d6a7', '#c8e6c9'])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show()