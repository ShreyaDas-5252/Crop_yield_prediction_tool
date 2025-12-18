import mysql.connector
from config import DB_CONFIG

def setup_database():
    """Setup database and tables"""
    try:
        # Connect without database to create it
        config = DB_CONFIG.copy()
        database = config.pop('database')
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cursor.execute(f"USE {database}")
        
        # Create predictions table
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
            sunlight_hours FLOAT,
            pesticide_usage FLOAT,
            farm_size FLOAT,
            elevation FLOAT,
            predicted_yield FLOAT,
            model_used VARCHAR(100),
            confidence FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create farms table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farms (
            farm_id INT AUTO_INCREMENT PRIMARY KEY,
            farmer_name VARCHAR(100),
            location VARCHAR(100),
            farm_size FLOAT,
            soil_type VARCHAR(50),
            irrigation_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create historical_yields table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_yields (
            id INT AUTO_INCREMENT PRIMARY KEY,
            farm_id INT,
            crop_type VARCHAR(50),
            actual_yield FLOAT,
            season VARCHAR(50),
            year INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farm_id) REFERENCES farms(farm_id)
        )
        """)
        
        print("Database setup completed successfully!")
        
    except mysql.connector.Error as e:
        print(f"Error setting up database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()