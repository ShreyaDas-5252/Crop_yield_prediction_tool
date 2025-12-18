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

def test_connection(host=None, user=None, password=None, database=None, port=3306):
    """Test database connection with given credentials"""
    try:
        connection_config = {
            "host": host or DB_CONFIG["host"],
            "user": user or DB_CONFIG["user"],
            "password": password or DB_CONFIG["password"],
            "database": database or DB_CONFIG["database"],
            "port": port or DB_CONFIG["port"]
        }
        
        conn = mysql.connector.connect(**connection_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Database connection test failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during connection test: {e}")
        return False

def save_prediction(prediction_data):
    """Save prediction to database with flexible column handling"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check which columns exist in the table
        cursor.execute("DESCRIBE predictions")
        existing_columns = [column[0] for column in cursor.fetchall()]
        
        # Build dynamic query based on available columns
        available_columns = []
        available_values = []
        
        # Required columns
        base_columns = {
            'crop': prediction_data.get('crop_type'),
            'rainfall': prediction_data.get('rainfall'),
            'temperature': prediction_data.get('temperature'),
            'humidity': prediction_data.get('humidity'),
            'soil_ph': prediction_data.get('soil_ph'),
            'fertilizer_kg_per_ha': prediction_data.get('fertilizer_kg_per_ha'),
            'predicted_yield': prediction_data.get('predicted_yield'),
            'model_used': prediction_data.get('model_used', 'random_forest')
        }
        
        # Optional columns (only include if they exist in table)
        optional_columns = {
            'soil_type': prediction_data.get('soil_type'),
            'irrigation': prediction_data.get('irrigation')
        }
        
        # Add base columns
        for col, value in base_columns.items():
            if col in existing_columns:
                available_columns.append(col)
                available_values.append(value)
        
        # Add optional columns only if they exist
        for col, value in optional_columns.items():
            if col in existing_columns and value is not None:
                available_columns.append(col)
                available_values.append(value)
        
        # Create the dynamic query
        columns_str = ', '.join(available_columns)
        placeholders = ', '.join(['%s'] * len(available_columns))
        
        query = f"INSERT INTO predictions ({columns_str}, created_at) VALUES ({placeholders}, %s)"
        available_values.append(datetime.now())
        
        cursor.execute(query, available_values)
        conn.commit()
        
        st.success(f"✅ Prediction saved successfully! (Used columns: {len(available_columns)})")
        return True
        
    except mysql.connector.Error as e:
        st.error(f"Error saving prediction: {e}")
        
        # If there's a column error, try with basic columns only
        if "Unknown column" in str(e):
            st.info("🔄 Retrying with basic columns only...")
            return save_prediction_basic(prediction_data)
        return False
    finally:
        if conn:
            conn.close()

def save_prediction_basic(prediction_data):
    """Save prediction with only basic columns (fallback method)"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = """
        INSERT INTO predictions 
        (crop, rainfall, temperature, humidity, soil_ph, fertilizer_kg_per_ha, 
         predicted_yield, model_used, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            prediction_data.get('crop_type'),
            prediction_data.get('rainfall'),
            prediction_data.get('temperature'),
            prediction_data.get('humidity'),
            prediction_data.get('soil_ph'),
            prediction_data.get('fertilizer_kg_per_ha'),
            prediction_data.get('predicted_yield'),
            prediction_data.get('model_used', 'random_forest'),
            datetime.now()
        )
        
        cursor.execute(query, values)
        conn.commit()
        st.success("✅ Prediction saved with basic columns!")
        return True
        
    except mysql.connector.Error as e:
        st.error(f"Error saving prediction (basic): {e}")
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
            stats[key] = cursor.fetchone()[0] or 0  # Handle None values
        
        return stats
        
    except Exception as e:
        st.error(f"Error fetching stats: {e}")
        return {
            'total_predictions': 0,
            'avg_yield': 0,
            'crop_count': 0,
            'recent_activity': 0
        }
    finally:
        if conn:
            conn.close()

def setup_database_tables():
    """Create necessary database tables if they don't exist"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create predictions table with all columns
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            crop VARCHAR(64),
            rainfall FLOAT,
            temperature FLOAT,
            humidity FLOAT,
            soil_ph FLOAT,
            fertilizer_kg_per_ha FLOAT,
            soil_type VARCHAR(50),
            irrigation VARCHAR(50),
            predicted_yield FLOAT,
            model_used VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Check if new columns need to be added
        cursor.execute("DESCRIBE predictions")
        existing_columns = [column[0] for column in cursor.fetchall()]
        
        # Add missing columns
        if 'soil_type' not in existing_columns:
            cursor.execute("ALTER TABLE predictions ADD COLUMN soil_type VARCHAR(50) AFTER fertilizer_kg_per_ha")
            st.info("✅ Added soil_type column to predictions table")
        
        if 'irrigation' not in existing_columns:
            cursor.execute("ALTER TABLE predictions ADD COLUMN irrigation VARCHAR(50) AFTER soil_type")
            st.info("✅ Added irrigation column to predictions table")
        
        conn.commit()
        st.success("✅ Database tables are up to date!")
        return True
        
    except Exception as e:
        st.error(f"Error setting up database tables: {e}")
        return False
    finally:
        if conn:
            conn.close()