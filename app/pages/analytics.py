import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.title("📈 Economic Analytics")
    
    # Economic Analysis Section
    st.header("💰 ROI Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        expected_yield = st.number_input("Expected Yield (tons/ha)", value=3.5, min_value=0.0, step=0.1)
    
    with col2:
        input_costs = st.number_input("Input Costs (₹/ha)", value=25000, min_value=0, step=1000)
    
    with col3:
        market_price = st.number_input("Market Price (₹/ton)", value=18000, min_value=0, step=1000)
    
    if st.button("Calculate ROI"):
        expected_revenue = expected_yield * market_price
        net_profit = expected_revenue - input_costs
        
        if input_costs > 0:
            roi_percentage = (net_profit / input_costs) * 100
        else:
            roi_percentage = 0
        
        if market_price > 0:
            break_even_yield = input_costs / market_price
        else:
            break_even_yield = 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Expected Revenue", f"₹{expected_revenue:,.0f}")
        
        with col2:
            st.metric("Net Profit", f"₹{net_profit:,.0f}")
        
        with col3:
            st.metric("ROI", f"{roi_percentage:.1f}%")
        
        with col4:
            st.metric("Break-even Yield", f"{break_even_yield:.2f} tons/ha")
    
    # Cost Breakdown
    st.header("📋 Cost Breakdown Analysis")
    
    costs_data = {
        'Category': ['Fertilizer', 'Seeds', 'Labor', 'Irrigation', 'Pesticides', 'Equipment'],
        'Cost (₹)': [8000, 5000, 7000, 3000, 2000, 5000]
    }
    
    costs_df = pd.DataFrame(costs_data)
    fig = px.pie(costs_df, values='Cost (₹)', names='Category', title='Cost Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Analysis
    st.header("⚠️ Risk Assessment")
    
    risk_factors = {
        "Factor": ["Drought", "Floods", "Pests", "Price Drop", "Disease"],
        "Probability": [0.3, 0.1, 0.4, 0.5, 0.2],
        "Impact": [0.8, 0.9, 0.6, 0.7, 0.5]
    }
    
    risk_df = pd.DataFrame(risk_factors)
    risk_df['Risk Score'] = risk_df['Probability'] * risk_df['Impact']
    
    fig = px.bar(risk_df, x='Factor', y='Risk Score', 
                 title='Risk Factor Analysis',
                 color='Risk Score')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show()