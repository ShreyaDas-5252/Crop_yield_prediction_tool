import streamlit as st
import pandas as pd
import plotly.express as px
from app.utils.database import get_all_predictions


def show():

    st.title("📊 Farmer Dashboard")
    st.markdown("### 🌾 Smart Crop Analytics Dashboard")
    st.caption("AI-powered insights for farmers")

    # ==============================
    # Fetch Data
    # ==============================

    predictions = get_all_predictions()

    if not predictions.empty:

        # ==============================
        # Crop Filter
        # ==============================

        crop_filter = st.selectbox(
            "🌱 Filter by Crop",
            ["All"] + list(predictions["crop"].unique())
        )

        if crop_filter != "All":
            predictions = predictions[predictions["crop"] == crop_filter]

        # ==============================
        # Key Metrics
        # ==============================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_yield = predictions["yield_t_per_ha"].mean()
            st.metric("Average Yield", f"{avg_yield:.2f} ton/ha")

        with col2:
            total_predictions = len(predictions)
            st.metric("Total Predictions", total_predictions)

        with col3:
            unique_crops = predictions["crop"].nunique()
            st.metric("Crops Analyzed", unique_crops)

        with col4:
            success_rate = (predictions["yield_t_per_ha"] > 2).mean()
            st.metric("High Yield Rate", f"{success_rate:.1%}")

        # ==============================
        # Charts Section
        # ==============================

        col1, col2 = st.columns(2)

        # Yield by Crop Chart
        with col1:

            crop_yield = (
                predictions.groupby("crop")["yield_t_per_ha"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                crop_yield,
                x="crop",
                y="yield_t_per_ha",
                color="yield_t_per_ha",
                title="🌾 Average Yield by Crop",
                labels={"yield_t_per_ha": "Yield (ton/ha)"}
            )

            st.plotly_chart(fig, use_container_width=True)

        # Yield Distribution
        with col2:

            fig = px.histogram(
                predictions,
                x="yield_t_per_ha",
                nbins=20,
                title="📊 Yield Distribution",
            )

            st.plotly_chart(fig, use_container_width=True)

        # ==============================
        # Risk Pie Chart
        # ==============================

        if "crop_extinction_risk" in predictions.columns:

            st.subheader("⚠ Crop Risk Distribution")

            risk_counts = (
                predictions["crop_extinction_risk"]
                .value_counts()
                .reset_index()
            )

            risk_counts.columns = ["Risk Level", "Count"]

            fig = px.pie(
                risk_counts,
                names="Risk Level",
                values="Count",
                title="Crop Extinction Risk Distribution",
                hole=0.4
            )

            st.plotly_chart(fig, use_container_width=True)

        # ==============================
        # Yield Trend Over Time
        # ==============================

        st.subheader("📈 Yield Trend Over Time")

        predictions["created_at"] = pd.to_datetime(predictions["created_at"])

        trend = (
            predictions.groupby(predictions["created_at"].dt.date)["yield_t_per_ha"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            trend,
            x="created_at",
            y="yield_t_per_ha",
            markers=True,
            title="Average Yield Trend",
            labels={"yield_t_per_ha": "Yield (ton/ha)"}
        )

        st.plotly_chart(fig, use_container_width=True)

        # ==============================
        # Recent Predictions Table
        # ==============================

        st.subheader("📊 Recent Predictions")

        st.dataframe(
            predictions[
                [
                    "crop",
                    "state",
                    "season",
                    "yield_t_per_ha",
                    "crop_extinction_risk",
                    "created_at",
                ]
            ].head(10),
            use_container_width=True,
        )

        # ==============================
        # Download CSV Button
        # ==============================

        st.download_button(
            label="⬇ Download Predictions CSV",
            data=predictions.to_csv(index=False),
            file_name="crop_predictions.csv",
            mime="text/csv",
        )

    else:

        st.info("No prediction data available. Make some predictions first!")


if __name__ == "__main__":
    show()