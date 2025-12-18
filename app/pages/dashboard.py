import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.utils.database import get_recent_predictions, get_yield_stats

def show():
    st.title("📊 Farmer Dashboard")
    
    # Fetch data
    predictions = get_recent_predictions(limit=100)
    stats = get_yield_stats()
    
    if not predictions.empty:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_yield = predictions['predicted_yield'].mean()
            st.metric("Average Yield", f"{avg_yield:.2f} tons/ha")
        
        with col2:
            total_predictions = len(predictions)
            st.metric("Total Predictions", total_predictions)
        
        with col3:
            unique_crops = predictions['crop'].nunique()
            st.metric("Crops Analyzed", unique_crops)
        
        with col4:
            success_rate = (predictions['predicted_yield'] > 2.0).mean()
            st.metric("Success Rate", f"{success_rate:.1%}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Yield by crop
            crop_yield = predictions.groupby('crop')['predicted_yield'].mean().reset_index()
            fig = px.bar(crop_yield, x='crop', y='predicted_yield',
                        title='Average Yield by Crop Type',
                        color='predicted_yield')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Yield distribution
            fig = px.histogram(predictions, x='predicted_yield',
                             title='Yield Distribution',
                             nbins=20,
                             color_discrete_sequence=['#4CAF50'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent predictions table
        st.subheader("Recent Predictions")
        st.dataframe(predictions[['crop', 'predicted_yield', 'created_at']].head(10), 
                    use_container_width=True)
    
    else:
        st.info("No prediction data available. Make some predictions first!")
        
        # Sample data for demonstration
        st.subheader("Sample Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            sample_data = pd.DataFrame({
                'Crop': ['Wheat', 'Rice', 'Corn', 'Soybean'],
                'Yield': [3.2, 4.1, 3.8, 2.9]
            })
            fig = px.bar(sample_data, x='Crop', y='Yield', title='Sample Crop Yields')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            trend_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Yield': [2.8, 3.1, 3.5, 3.2, 3.7, 4.0]
            })
            fig = px.line(trend_data, x='Month', y='Yield', title='Sample Yield Trend')
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show()