import mysql.connector
import pandas as pd
from datetime import datetime
import streamlit as st
from config import DB_CONFIG

# ==============================
# Database Connection
# ==============================

def get_connection():
    """Create database connection using config"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
        return None

# ==============================
# Save Prediction
# ==============================

def save_prediction(data):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO predictions
        (crop, state, season, rainfall_mm, temperature_c, humidity_percent, 
        soil_ph, soil_nitrogen, soil_phosphorus, soil_potassium, soil_moisture, 
        solar_radiation, ndvi, yield_t_per_ha, yield_kg_per_ha, 
        crop_extinction_risk, model_used, created_at)
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
    except Exception as e:
        st.error(f"Database save error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# ==============================
# Fetch ALL Predictions
# ==============================

def get_all_predictions():
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        query = "SELECT * FROM predictions ORDER BY created_at DESC"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching predictions: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# ==============================
# Yield Statistics
# ==============================

def get_yield_stats():
    conn = get_connection()
    if conn is None:
        return {}

    try:
        cursor = conn.cursor()
        queries = {
            "total_predictions": "SELECT COUNT(*) FROM predictions",
            "avg_yield": "SELECT AVG(yield_t_per_ha) FROM predictions",
            "crop_count": "SELECT COUNT(DISTINCT crop) FROM predictions",
            "recent_activity": "SELECT COUNT(*) FROM predictions WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)"
        }

        stats = {}
        for key, query in queries.items():
            cursor.execute(query)
            result = cursor.fetchone()[0]
            stats[key] = result if result is not None else 0
        return stats
    except Exception as e:
        st.error(f"Error fetching stats: {e}")
        return {}
    finally:
        if conn:
            conn.close()

# ==============================
# Setup Database Table (FIXED NAME)
# ==============================

def setup_database_tables():
    """Renamed from setup_database to match your interface expectations"""
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            crop VARCHAR(50),
            state VARCHAR(50),
            season VARCHAR(20),
            rainfall_mm FLOAT,
            temperature_c FLOAT,
            humidity_percent FLOAT,
            soil_ph FLOAT,
            soil_nitrogen FLOAT,
            soil_phosphorus FLOAT,
            soil_potassium FLOAT,
            soil_moisture FLOAT,
            solar_radiation FLOAT,
            ndvi FLOAT,
            yield_t_per_ha FLOAT,
            yield_kg_per_ha FLOAT,
            crop_extinction_risk VARCHAR(20),
            model_used VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        st.success("✅ Database table ready")
    except Exception as e:
        st.error(f"Database setup error: {e}")
    finally:
        if conn:
            conn.close()

# ==============================
# Test Database Connection (FIXED ARGUMENTS)
# ==============================

def test_connection():
    """
    Simplified to use DB_CONFIG directly so the Settings page 
    doesn't fail with 'missing 4 arguments'
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        conn.close()
        return True
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return False