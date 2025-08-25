import mysql.connector
from mysql.connector import pooling
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self._create_pool()
    
    def _create_pool(self):
        """Create connection pool for database"""
        try:
            pool_config = {
                'host': Config.DB_HOST,
                'user': Config.DB_USER,
                'password': Config.DB_PASSWORD,
                'database': Config.DB_NAME,
                'pool_name': 'zomato_pool',
                'pool_size': 5,
                'autocommit': False
            }
            self.pool = mysql.connector.pooling.MySQLConnectionPool(**pool_config)
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create database pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            return self.pool.get_connection()
        except Exception as e:
            logger.error(f"Failed to get database connection: {e}")
            raise
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and return results if fetch=True"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.rowcount
                
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database query failed: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# Global database manager instance
db_manager = DatabaseManager()
