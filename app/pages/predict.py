import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from app.utils.database import save_prediction

def show():
    st.title("🌾 Yield Prediction")
    
    # Load model function
    @st.cache_resource
    def load_model():
        try:
            model_path = "app/models/model.pkl"
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                st.success("✅ Model loaded successfully!")
                return model
            else:
                st.error("❌ Model file not found. Please train the model first.")
                return None
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            return None
    
    model = load_model()
    
    # Input form
    with st.form("prediction_form"):
        st.subheader("Farm Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            crop_type = st.selectbox("Crop Type", 
                                   ["Wheat", "Rice", "Corn", "Soybean", "Cotton", "Sugarcane"])
            rainfall = st.slider("Rainfall (mm)", 0.0, 2000.0, 500.0, step=10.0)
            temperature = st.slider("Temperature (°C)", 0.0, 40.0, 25.0, step=0.5)
            humidity = st.slider("Humidity (%)", 0.0, 100.0, 60.0, step=1.0)
        
        with col2:
            soil_ph = st.slider("Soil pH", 4.0, 9.0, 6.5, step=0.1)
            fertilizer = st.slider("Fertilizer (kg/ha)", 0.0, 500.0, 100.0, step=5.0)
            soil_type = st.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Silty"])
            irrigation = st.selectbox("Irrigation", ["Drip", "Sprinkler", "Flood", "None"])
        
        submitted = st.form_submit_button("Predict Yield", use_container_width=True)
    
    if submitted:
        if model is None:
            st.error("Cannot make prediction - model not available. Please train the model first.")
            return
        
        try:
            # Prepare input data with multiple possible feature names
            input_data = {
                'crop_type': crop_type,
                'crop': crop_type,  # Alternative name
                'rainfall': rainfall,
                'temperature': temperature,
                'temp': temperature,  # Alternative name
                'humidity': humidity,
                'soil_ph': soil_ph,
                'ph': soil_ph,  # Alternative name
                'fertilizer_kg_per_ha': fertilizer,
                'fertilizer': fertilizer,  # Alternative name
                'soil_type': soil_type,
                'irrigation': irrigation
            }
            
            # Convert to DataFrame
            input_df = pd.DataFrame([input_data])
            
            # Debug: Show what features we have
            st.info(f"Available features: {list(input_df.columns)}")
            
            # Get the features the model expects
            if hasattr(model, 'feature_names_in_'):
                expected_features = model.feature_names_in_
                st.info(f"Model expects: {list(expected_features)}")
            else:
                # If model doesn't have feature names, use common ones
                expected_features = ['rainfall', 'temperature', 'humidity', 'soil_ph', 'fertilizer_kg_per_ha']
                st.warning("Model doesn't have feature names. Using default features.")
            
            # Map categorical variables to numbers
            crop_mapping = {'Wheat': 0, 'Rice': 1, 'Corn': 2, 'Soybean': 3, 'Cotton': 4, 'Sugarcane': 5}
            soil_mapping = {'Loamy': 0, 'Sandy': 1, 'Clay': 2, 'Silty': 3, 'Peaty': 4, 'Chalky': 5}
            irrigation_mapping = {'Drip': 0, 'Sprinkler': 1, 'Flood': 2, 'None': 3}
            
            # Apply mappings
            if 'crop_type' in input_df.columns:
                input_df['crop_type'] = input_df['crop_type'].map(crop_mapping).fillna(0)
            if 'crop' in input_df.columns:
                input_df['crop'] = input_df['crop'].map(crop_mapping).fillna(0)
            if 'soil_type' in input_df.columns:
                input_df['soil_type'] = input_df['soil_type'].map(soil_mapping).fillna(0)
            if 'irrigation' in input_df.columns:
                input_df['irrigation'] = input_df['irrigation'].map(irrigation_mapping).fillna(0)
            
            # Select only the features that the model expects
            available_features = []
            for feature in expected_features:
                if feature in input_df.columns:
                    available_features.append(feature)
                else:
                    st.warning(f"Feature '{feature}' not found in input data")
            
            if not available_features:
                st.error("No compatible features found between input and model!")
                return
            
            input_df = input_df[available_features]
            
            # Ensure we have the same features as the model
            if hasattr(model, 'feature_names_in_'):
                # Reorder columns to match model expectations
                input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)
            
            st.info(f"Using features: {list(input_df.columns)}")
            
            # Make prediction
            prediction = model.predict(input_df)[0]
            
            # Display results
            st.success("🎯 Prediction completed successfully!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Predicted Yield", f"{prediction:.2f} tons/ha")
            
            with col2:
                # Calculate confidence based on input quality
                confidence_factors = []
                if 300 <= rainfall <= 1200:
                    confidence_factors.append(1.0)
                if 6.0 <= soil_ph <= 7.5:
                    confidence_factors.append(1.0)
                if 50 <= fertilizer <= 200:
                    confidence_factors.append(1.0)
                
                confidence = 0.7 + (len(confidence_factors) * 0.1)  # Base 70% + 10% per good factor
                confidence = min(confidence, 0.95)
                st.metric("Confidence", f"{confidence:.1%}")
            
            with col3:
                # Compare with average
                avg_yields = {"Wheat": 3.0, "Rice": 4.0, "Corn": 3.5, "Soybean": 2.5, "Cotton": 1.5, "Sugarcane": 70.0}
                avg_yield = avg_yields.get(crop_type, 3.0)
                diff = ((prediction - avg_yield) / avg_yield) * 100
                st.metric("Vs Average", f"{diff:+.1f}%")
            
            # Save to database
            try:
                save_prediction({
                    'crop_type': crop_type,
                    'rainfall': rainfall,
                    'temperature': temperature,
                    'humidity': humidity,
                    'soil_ph': soil_ph,
                    'fertilizer_kg_per_ha': fertilizer,
                    'soil_type': soil_type,
                    'irrigation': irrigation,
                    'predicted_yield': prediction,
                    'model_used': 'random_forest'
                })
                st.info("📊 Prediction saved to database")
            except Exception as e:
                st.warning(f"Could not save to database: {e}")
            
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")
            st.info("💡 **Troubleshooting tips:**")
            st.info("1. Make sure the model was trained recently")
            st.info("2. Check if feature names match between training and prediction")
            st.info("3. Try retraining the model with the current dataset")

if __name__ == "__main__":
    show()