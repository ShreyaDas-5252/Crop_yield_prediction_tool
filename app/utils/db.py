import mysql.connector
import pandas as pd
from datetime import datetime
import streamlit as st
from config import DB_CONFIG

def get_connection():
    """Create database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def save_prediction(prediction_data):
    """Save prediction to database"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = """
        INSERT INTO predictions 
        (crop, rainfall, temperature, humidity, soil_ph, fertilizer_kg_per_ha, 
         soil_type, irrigation, sunlight_hours, pesticide_usage, farm_size, elevation,
         predicted_yield, model_used, confidence, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            prediction_data.get('crop_type'),
            prediction_data.get('rainfall'),
            prediction_data.get('temperature'),
            prediction_data.get('humidity'),
            prediction_data.get('soil_ph'),
            prediction_data.get('fertilizer_kg_per_ha'),
            prediction_data.get('soil_type'),
            prediction_data.get('irrigation'),
            prediction_data.get('sunlight_hours'),
            prediction_data.get('pesticide_usage'),
            prediction_data.get('farm_size'),
            prediction_data.get('elevation'),
            prediction_data.get('predicted_yield'),
            prediction_data.get('model_used', 'advanced_ensemble'),
            prediction_data.get('confidence', 0.85),
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

def get_recent_predictions(limit=50):
    """Get recent predictions from database"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = f"SELECT * FROM predictions ORDER BY created_at DESC LIMIT {limit}"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching predictions: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def get_yield_stats():
    """Get yield statistics from database"""
    conn = get_connection()
    if conn is None:
        return {}
    
    try:
        cursor = conn.cursor()
        
        queries = {
            'total_predictions': "SELECT COUNT(*) FROM predictions",
            'avg_yield': "SELECT AVG(predicted_yield) FROM predictions",
            'crop_count': "SELECT COUNT(DISTINCT crop) FROM predictions",
            'recent_activity': "SELECT COUNT(*) FROM predictions WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)"
        }
        
        stats = {}
        for key, query in queries.items():
            cursor.execute(query)
            stats[key] = cursor.fetchone()[0]
        
        return stats
        
    except Exception as e:
        st.error(f"Error fetching stats: {e}")
        return {}
    finally:
        if conn:
            conn.close()

def test_connection(host, user, password, database, port=3306):
    """Test database connection"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        conn.close()
        return True
    except:
        return False