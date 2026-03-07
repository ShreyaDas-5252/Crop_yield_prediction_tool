import mysql.connector
import pandas as pd
from datetime import datetime
import streamlit as st
from config import DB_CONFIG


# ===============================
# DATABASE CONNECTION
# ===============================

def get_connection():

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn

    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
        return None


# ===============================
# SAVE PREDICTION
# ===============================

def save_prediction(data):

    conn = get_connection()

    if conn is None:
        return False

    try:

        cursor = conn.cursor()

        query = """
        INSERT INTO predictions (

            crop,
            state,
            season,

            rainfall_mm,
            temperature_c,
            humidity_percent,

            soil_ph,
            soil_nitrogen,
            soil_phosphorus,
            soil_potassium,
            soil_moisture,

            solar_radiation,
            ndvi,

            yield_t_per_ha,
            yield_kg_per_ha,

            crop_extinction_risk,
            model_used,
            created_at

        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (

            data.get("crop"),
            data.get("state"),
            data.get("season"),

            data.get("rainfall_mm"),
            data.get("temperature_c"),
            data.get("humidity_percent"),

            data.get("soil_ph"),
            data.get("soil_nitrogen"),
            data.get("soil_phosphorus"),
            data.get("soil_potassium"),
            data.get("soil_moisture"),

            data.get("solar_radiation"),
            data.get("ndvi"),

            data.get("yield_t_per_ha"),
            data.get("yield_kg_per_ha"),

            data.get("crop_extinction_risk"),
            data.get("model_used"),

            datetime.now()
        )

        cursor.execute(query, values)

        conn.commit()

        return True

    except mysql.connector.Error as e:

        st.error(f"Error saving prediction: {e}")
        return False

    finally:

        if conn:
            conn.close()


# ===============================
# FETCH ALL PREDICTIONS
# ===============================

def get_all_predictions():

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    try:

        query = """
        SELECT

        crop,
        state,
        season,

        rainfall_mm,
        temperature_c,
        humidity_percent,

        soil_ph,
        soil_nitrogen,
        soil_phosphorus,
        soil_potassium,
        soil_moisture,

        solar_radiation,
        ndvi,

        yield_t_per_ha,
        yield_kg_per_ha,

        crop_extinction_risk,
        created_at

        FROM predictions
        ORDER BY created_at DESC
        """

        df = pd.read_sql(query, conn)

        return df

    except Exception as e:

        st.error(f"Error fetching predictions: {e}")
        return pd.DataFrame()

    finally:

        if conn:
            conn.close()


# ===============================
# DATABASE STATS
# ===============================

def get_yield_stats():

    conn = get_connection()

    if conn is None:
        return {}

    try:

        cursor = conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) FROM predictions")
        stats["total_predictions"] = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(yield_t_per_ha) FROM predictions")
        stats["avg_yield"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT crop) FROM predictions")
        stats["crop_count"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM predictions WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)"
        )

        stats["recent_activity"] = cursor.fetchone()[0]

        return stats

    except Exception as e:

        st.error(f"Stats error: {e}")
        return {}

    finally:

        if conn:
            conn.close()