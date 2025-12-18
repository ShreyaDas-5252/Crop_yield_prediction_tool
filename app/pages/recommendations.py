import streamlit as st
import pandas as pd

def show():
    st.title("💡 Smart Recommendations")
    
    # Input form for personalized recommendations
    with st.form("recommendation_form"):
        st.subheader("Your Farm Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop_type = st.selectbox("Primary Crop", 
                                   ["Wheat", "Rice", "Corn", "Soybean", "Cotton", "Sugarcane"])
            soil_type = st.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Silty"])
            region = st.selectbox("Region", ["North", "South", "East", "West", "Central"])
        
        with col2:
            budget = st.number_input("Available Budget (₹)", value=50000, min_value=0, step=5000)
            experience = st.selectbox("Farming Experience", 
                                    ["Beginner (<2 years)", "Intermediate (2-5 years)", "Expert (>5 years)"])
            irrigation = st.selectbox("Irrigation System", ["Drip", "Sprinkler", "Flood", "None"])
        
        submitted = st.form_submit_button("Generate Recommendations")
    
    if submitted:
        st.success("✅ Generating personalized recommendations...")
        
        # Generate recommendations based on inputs
        recommendations = generate_recommendations(crop_type, soil_type, region, budget, experience, irrigation)
        
        # Display recommendations
        for i, rec in enumerate(recommendations, 1):
            with st.expander(f"🎯 Recommendation #{i}: {rec['title']}", expanded=True):
                st.write(f"**Impact:** {rec['impact']}")
                st.write(f"**Implementation:** {rec['implementation']}")
                st.write(f"**Cost:** {rec['cost']}")
                st.write(f"**Timeline:** {rec['timeline']}")
                
                if st.button(f"Implement Recommendation #{i}", key=f"btn_{i}"):
                    st.success(f"✅ Implementation started for: {rec['title']}")

def generate_recommendations(crop, soil, region, budget, experience, irrigation):
    """Generate personalized farming recommendations"""
    
    base_recommendations = [
        {
            "title": "Soil Nutrient Management",
            "impact": "Increase yield by 15-20% and improve soil health",
            "implementation": f"Apply organic compost and balanced NPK fertilizers for {crop}. Test soil every 6 months.",
            "cost": "₹5,000 - ₹15,000 per hectare",
            "timeline": "Immediate (before next planting season)"
        },
        {
            "title": "Water Management Optimization",
            "impact": "Reduce water usage by 30% and increase yield by 10%",
            "implementation": f"Upgrade to {irrigation if irrigation != 'None' else 'drip'} irrigation with moisture sensors",
            "cost": "₹20,000 - ₹50,000 per hectare",
            "timeline": "2-4 weeks"
        },
        {
            "title": "Crop Rotation Plan",
            "impact": "Improve soil fertility and reduce pest incidence by 25%",
            "implementation": f"Rotate {crop} with leguminous crops like pulses or beans",
            "cost": "Minimal (seed cost only)",
            "timeline": "Next planting season"
        }
    ]
    
    # Add specific recommendations based on inputs
    if soil == "Sandy":
        base_recommendations.append({
            "title": "Soil Amendment for Sandy Soil",
            "impact": "Improve water retention and nutrient holding capacity by 40%",
            "implementation": "Add organic matter and clay content to soil. Use cover crops.",
            "cost": "₹8,000 - ₹12,000 per hectare",
            "timeline": "Before next planting season"
        })
    
    if irrigation == "None":
        base_recommendations.append({
            "title": "Basic Irrigation System Setup",
            "impact": "Ensure consistent water supply and reduce dependency on rainfall",
            "implementation": "Install simple sprinkler or drip irrigation system",
            "cost": "₹15,000 - ₹30,000 per hectare",
            "timeline": "3-5 weeks"
        })
    
    if experience == "Beginner (<2 years)":
        base_recommendations.append({
            "title": "Farming Training Program",
            "impact": "Build fundamental knowledge and improve farming practices",
            "implementation": "Enroll in local agricultural extension program or online courses",
            "cost": "Free - ₹2,000",
            "timeline": "Ongoing"
        })
    
    # Filter by budget
    affordable_recommendations = []
    for rec in base_recommendations:
        # Extract cost range and check if affordable
        cost_text = rec['cost']
        if '₹' in cost_text:
            costs = [int(x.replace(',', '')) for x in cost_text.split('₹')[1].split(' - ')[0].split() if x.replace(',', '').isdigit()]
            if costs and max(costs) <= budget:
                affordable_recommendations.append(rec)
        else:
            affordable_recommendations.append(rec)
    
    return affordable_recommendations[:4]  # Return top 4 recommendations

if __name__ == "__main__":
    show()