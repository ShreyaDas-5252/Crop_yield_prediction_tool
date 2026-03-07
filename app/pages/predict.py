import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

from app.utils.database import save_prediction
from app.utils.database import get_all_predictions


def show():
    st.title("🌾 Crop Yield & Risk Prediction")

    # ==============================
    # Load Models
    # ==============================

    @st.cache_resource
    def load_models():

        yield_model_path = "app/models/model.pkl"
        risk_model_path = "app/models/risk_model.pkl"

        yield_model = None
        risk_model = None

        if os.path.exists(yield_model_path):
            yield_model = joblib.load(yield_model_path)

        if os.path.exists(risk_model_path):
            risk_model = joblib.load(risk_model_path)

        return yield_model, risk_model


    yield_model, risk_model = load_models()

    if yield_model is None:
        st.error("❌ Yield model not found. Please train the model first.")
        return


    # ==============================
    # Input Form
    # ==============================

    with st.form("prediction_form"):

        st.subheader("🌱 Farm & Environment Details")

        col1, col2 = st.columns(2)

        with col1:

            crop = st.selectbox(
                "Crop",
                ["Rice", "Wheat", "Maize", "Soybean", "Sugarcane", "Cotton"]
            )

            state = st.selectbox(
                "State",
                ["Punjab", "Haryana", "Uttar Pradesh", "Bihar", "Maharashtra", "Karnataka"]
            )

            season = st.selectbox(
                "Season",
                ["Kharif", "Rabi", "Zaid"]
            )

            rainfall = st.slider(
                "Rainfall (mm)",
                0.0, 2000.0, 500.0
            )

            temperature = st.slider(
                "Temperature (°C)",
                0.0, 50.0, 25.0
            )

            humidity = st.slider(
                "Humidity (%)",
                0.0, 100.0, 60.0
            )

        with col2:

            soil_ph = st.slider(
                "Soil pH",
                4.0, 9.0, 6.5
            )

            soil_nitrogen = st.slider(
                "Soil Nitrogen",
                0.0, 150.0, 50.0
            )

            soil_phosphorus = st.slider(
                "Soil Phosphorus",
                0.0, 150.0, 40.0
            )

            soil_potassium = st.slider(
                "Soil Potassium",
                0.0, 200.0, 60.0
            )

            soil_moisture = st.slider(
                "Soil Moisture",
                0.0, 100.0, 40.0
            )

            solar_radiation = st.slider(
                "Solar Radiation",
                0.0, 30.0, 15.0
            )

            ndvi = st.slider(
                "NDVI (Vegetation Health Index)",
                0.0, 1.0, 0.6
            )

            irrigation = st.selectbox(
                "Irrigation Level",
                ["Low", "Medium", "High"]
            )

        submitted = st.form_submit_button("🔍 Predict")


    # ==============================
    # Prediction
    # ==============================

    if submitted:

        try:

            irrigation_map = {
                "Low": 0,
                "Medium": 1,
                "High": 2
            }

            input_data = {

                "crop": crop,
                "state": state,
                "season": season,
                "rainfall_mm": rainfall,
                "temperature_c": temperature,
                "humidity_percent": humidity,
                "soil_ph": soil_ph,
                "soil_nitrogen": soil_nitrogen,
                "soil_phosphorus": soil_phosphorus,
                "soil_potassium": soil_potassium,
                "soil_moisture": soil_moisture,
                "solar_radiation": solar_radiation,
                "ndvi": ndvi,
                "irrigation_level": irrigation_map[irrigation]

            }

            input_df = pd.DataFrame([input_data])

            # Encode categorical columns
            categorical_cols = ["crop", "state", "season"]

            for col in categorical_cols:
                input_df[col] = input_df[col].astype("category").cat.codes

            # Align features with model
            if hasattr(yield_model, "feature_names_in_"):

                input_df = input_df.reindex(
                    columns=yield_model.feature_names_in_,
                    fill_value=0
                )

            # ==============================
            # Make Predictions
            # ==============================

            yield_prediction = yield_model.predict(input_df)[0]

            risk_prediction = None

            if risk_model is not None:
                risk_prediction = risk_model.predict(input_df)[0]

            # ==============================
            # Display Results
            # ==============================

            st.success("✅ Prediction Successful")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Yield (ton/ha)",
                    f"{yield_prediction:.2f}"
                )

            with col2:

                st.metric(
                    "Yield (kg/ha)",
                    f"{yield_prediction * 1000:.0f}"
                )

            with col3:

                if risk_prediction is not None:

                    st.metric(
                        "Crop Extinction Risk",
                        risk_prediction
                    )

                else:

                    st.metric(
                        "Crop Extinction Risk",
                        "N/A"
                    )

            st.info("NDVI measures vegetation health using satellite imagery.")


            # ==============================
            # Save Prediction
            # ==============================

            try:

                save_prediction({

                    "crop": crop,
                    "state": state,
                    "season": season,
                    "rainfall_mm": rainfall,
                    "temperature_c": temperature,
                    "humidity_percent": humidity,
                    "soil_ph": soil_ph,
                    "soil_nitrogen": soil_nitrogen,
                    "soil_phosphorus": soil_phosphorus,
                    "soil_potassium": soil_potassium,
                    "soil_moisture": soil_moisture,
                    "solar_radiation": solar_radiation,
                    "ndvi": ndvi,
                    "yield_t_per_ha": yield_prediction,
                    "yield_kg_per_ha": yield_prediction * 1000,
                    "crop_extinction_risk": risk_prediction,
                    "model_used": "random_forest"

                })

                st.success("📊 Prediction stored in database")

            except Exception as e:

                st.warning(f"Database save error: {e}")

        except Exception as e:

            st.error(f"Prediction error: {e}")


    # ==============================
    # SHOW STORED PREDICTIONS TABLE
    # ==============================

    st.divider()
    st.subheader("📊 Stored Predictions")

    try:

        df = get_all_predictions()

        if not df.empty:

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info("No stored predictions found.")

    except Exception as e:

        st.error(f"Error loading predictions: {e}")


if __name__ == "__main__":
    show()