import mysql.connector
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """Migrate database to fix schema issues"""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = connection.cursor()
        
        # Check if items table has category column
        cursor.execute("DESCRIBE items")
        columns = [column[0] for column in cursor.fetchall()]
        
        if 'category' not in columns:
            logger.info("Adding category column to items table...")
            cursor.execute("ALTER TABLE items ADD COLUMN category VARCHAR(50) DEFAULT NULL")
        
        if 'image_url' not in columns:
            logger.info("Adding image_url column to items table...")
            cursor.execute("ALTER TABLE items ADD COLUMN image_url VARCHAR(500) DEFAULT NULL")
        
        # Check if orders table has order_timestamp column
        cursor.execute("DESCRIBE orders")
        order_columns = [column[0] for column in cursor.fetchall()]
        
        if 'order_timestamp' not in order_columns:
            logger.info("Adding order_timestamp column to orders table...")
            cursor.execute("ALTER TABLE orders ADD COLUMN order_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Update existing items with category if they don't have one
        cursor.execute("UPDATE items SET category = 'Main Course' WHERE category IS NULL")
        
        connection.commit()
        logger.info("Database migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    migrate_database()
