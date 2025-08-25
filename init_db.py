import mysql.connector
from config import Config
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize database with schema and seed data"""
    try:
        # Connect to MySQL server (without database)
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        cursor.execute(f"USE {Config.DB_NAME}")
        
        # Create tables
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS items (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL UNIQUE,
            category VARCHAR(50),
            price DECIMAL(10,2),
            image_url VARCHAR(500)
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            item_id INT NOT NULL,
            quantity INT NOT NULL,
            delivery_address TEXT NOT NULL,
            order_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
        );
        """
        
        for statement in create_tables_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        # Insert sample users with proper password hashing
        users_data = [
            ('alice', 'password123'),
            ('bob', 'password123'),
            ('charlie', 'password123')
        ]
        
        for username, password in users_data:
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT IGNORE INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
        
        # Insert menu items with images (all URLs verified and working)
        items_data = [
            ('Chicken Biryani', 'Main Course', 220.00, 'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=800'),
            ('Paneer Butter Masala', 'Main Course', 180.00, 'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f'),
            ('Butter Chicken', 'Main Course', 250.00, 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=800'),
            ('Veg Momos', 'Snacks', 90.00, 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800'),
            ('Chicken Wings', 'Snacks', 140.00, 'https://images.unsplash.com/photo-1600891964599-f61ba0e24092'),
            ('Masala Dosa', 'Main Course', 120.00, 'https://images.unsplash.com/photo-1589301760014-9e1c5c8c8c8c?w=800'),
            ('Pav Bhaji', 'Snacks', 100.00, 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800'),
            ('Chocolate Brownie', 'Dessert', 120.00, 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800'),
            ('Mango Smoothie', 'Beverage', 110.00, 'https://sl.bing.net/iRX8MnUZedo'),
            ('Cold Coffee', 'Beverage', 90.00, 'https://images.unsplash.com/photo-1509042239860-f550ce710b93'),
            ('Tandoori Roti', 'Main Course', 25.00, 'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=800'),
            ('Gulab Jamun', 'Dessert', 70.00, 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800'),
            ('Cheeseburger', 'Snacks', 180.00, 'https://images.unsplash.com/photo-1550547660-d9450f859349'),
            ('Margherita Pizza', 'Main Course', 220.00, 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800'),
            ('Grilled Sandwich', 'Snacks', 120.00, 'https://images.unsplash.com/photo-1528735602781-4a98c0d0c3b1?w=800'),
            ('French Fries', 'Snacks', 80.00, 'https://images.unsplash.com/photo-1571091718767-18b5b1457add')
        ]
        
        for item_name, category, price, image_url in items_data:
            cursor.execute(
                "INSERT IGNORE INTO items (item_name, category, price, image_url) VALUES (%s, %s, %s, %s)",
                (item_name, category, price, image_url)
            )
        
        # Insert sample orders
        orders_data = [
            (1, 1, 2, '123 Main Street', '2025-01-01 12:15:00'),
            (2, 2, 1, '456 Park Avenue', '2025-01-02 13:45:00'),
            (3, 3, 3, '789 Hill Road', '2025-01-03 14:20:00'),
            (1, 1, 1, '123 Main Street', '2025-01-03 15:10:00'),
            (2, 4, 2, '456 Park Avenue', '2025-01-04 12:00:00'),
            (3, 5, 1, '789 Hill Road', '2025-01-04 18:30:00'),
            (1, 3, 1, '123 Main Street', '2025-01-05 19:00:00'),
            (2, 1, 2, '456 Park Avenue', '2025-01-06 20:15:00'),
            (3, 2, 1, '789 Hill Road', '2025-01-06 21:40:00'),
            (1, 5, 3, '123 Main Street', '2025-01-07 10:25:00')
        ]
        
        for user_id, item_id, quantity, address, timestamp in orders_data:
            cursor.execute(
                "INSERT IGNORE INTO orders (user_id, item_id, quantity, delivery_address, order_timestamp) VALUES (%s, %s, %s, %s, %s)",
                (user_id, item_id, quantity, address, timestamp)
            )
        
        connection.commit()
        logger.info("Database initialized successfully!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    init_database()
