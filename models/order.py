from models.database import db_manager
from datetime import datetime, timedelta
import re

class Order:
    def __init__(self, order_id=None, user_id=None, item_id=None, quantity=None, 
                 delivery_address=None, order_timestamp=None, item_name=None, category=None, price=None):
        self.order_id = order_id
        self.user_id = user_id
        self.item_id = item_id
        self.quantity = quantity
        self.delivery_address = delivery_address
        self.order_timestamp = order_timestamp
        self.item_name = item_name
        self.category = category
        self.price = price
    
    @staticmethod
    def validate_address(address):
        """Validate delivery address"""
        if not address or len(address.strip()) < 10:
            return False, "Delivery address must be at least 10 characters long"
        
        # Basic sanitization
        address = re.sub(r'[<>"\']', '', address.strip())
        return True, address
    
    @staticmethod
    def validate_quantity(quantity):
        """Validate quantity"""
        try:
            qty = int(quantity)
            if qty <= 0 or qty > 100:
                return False, "Quantity must be between 1 and 100"
            return True, qty
        except (ValueError, TypeError):
            return False, "Quantity must be a valid number"
    
    @staticmethod
    def create_order(user_id, item_id, quantity, delivery_address):
        """Create a new order"""
        # Validate inputs
        valid_quantity, quantity_error = Order.validate_quantity(quantity)
        if not valid_quantity:
            raise ValueError(quantity_error)
        
        valid_address, address_error = Order.validate_address(delivery_address)
        if not valid_address:
            raise ValueError(address_error)
        
        # Check if item exists
        item_query = "SELECT * FROM items WHERE item_id = %s"
        item_result = db_manager.execute_query(item_query, (item_id,), fetch=True)
        if not item_result:
            raise ValueError("Item not found")
        
        # Create order
        query = """
            INSERT INTO orders (user_id, item_id, quantity, delivery_address)
            VALUES (%s, %s, %s, %s)
        """
        db_manager.execute_query(query, (user_id, item_id, valid_quantity, address_error))
        
        return True
    
    @staticmethod
    def get_user_orders(user_id, limit=None, offset=0):
        """Get orders for a specific user"""
        query = """
            SELECT o.*, i.item_name, i.category, i.price
            FROM orders o
            JOIN items i ON o.item_id = i.item_id
            WHERE o.user_id = %s
            ORDER BY o.order_timestamp DESC
        """
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        result = db_manager.execute_query(query, (user_id,), fetch=True)
        
        orders = []
        for row in result:
            order = Order(
                order_id=row['order_id'],
                user_id=row['user_id'],
                item_id=row['item_id'],
                quantity=row['quantity'],
                delivery_address=row['delivery_address'],
                order_timestamp=row['order_timestamp'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price']
            )
            orders.append(order)
        
        return orders
    
    @staticmethod
    def get_all_orders(limit=None, offset=0):
        """Get all orders with item details"""
        query = """
            SELECT o.*, i.item_name, i.category, i.price, u.username
            FROM orders o
            JOIN items i ON o.item_id = i.item_id
            JOIN users u ON o.user_id = u.user_id
            ORDER BY o.order_timestamp DESC
        """
        
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        result = db_manager.execute_query(query, fetch=True)
        
        orders = []
        for row in result:
            order = Order(
                order_id=row['order_id'],
                user_id=row['user_id'],
                item_id=row['item_id'],
                quantity=row['quantity'],
                delivery_address=row['delivery_address'],
                order_timestamp=row['order_timestamp'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price']
            )
            orders.append(order)
        
        return orders
    
    @staticmethod
    def delete_order(order_id, user_id):
        """Delete an order (only if it belongs to the user)"""
        query = "DELETE FROM orders WHERE order_id = %s AND user_id = %s"
        affected_rows = db_manager.execute_query(query, (order_id, user_id))
        return affected_rows > 0
    
    @staticmethod
    def update_order(order_id, user_id, quantity, delivery_address):
        """Update an order"""
        # Validate inputs
        valid_quantity, quantity_error = Order.validate_quantity(quantity)
        if not valid_quantity:
            raise ValueError(quantity_error)
        
        valid_address, address_error = Order.validate_address(delivery_address)
        if not valid_address:
            raise ValueError(address_error)
        
        query = """
            UPDATE orders 
            SET quantity = %s, delivery_address = %s
            WHERE order_id = %s AND user_id = %s
        """
        affected_rows = db_manager.execute_query(query, (valid_quantity, address_error, order_id, user_id))
        return affected_rows > 0
    
    # Analytics methods
    @staticmethod
    def get_total_orders():
        """Get total number of orders"""
        query = "SELECT COUNT(*) as total FROM orders"
        result = db_manager.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def get_popular_dishes(limit=5):
        """Get most popular dishes"""
        query = """
            SELECT i.item_name, i.category, i.price, 
                   SUM(o.quantity) as total_ordered,
                   COUNT(o.order_id) as order_count
            FROM orders o
            JOIN items i ON o.item_id = i.item_id
            GROUP BY i.item_id, i.item_name, i.category, i.price
            ORDER BY total_ordered DESC
            LIMIT %s
        """
        return db_manager.execute_query(query, (limit,), fetch=True)
    
    @staticmethod
    def get_orders_per_day(days=7):
        """Get orders per day for the last N days"""
        query = """
            SELECT DATE(order_timestamp) as order_date,
                   COUNT(*) as order_count
            FROM orders
            WHERE order_timestamp >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY DATE(order_timestamp)
            ORDER BY order_date
        """
        return db_manager.execute_query(query, (days,), fetch=True)
    
    @staticmethod
    def get_orders_by_category():
        """Get orders grouped by category"""
        query = """
            SELECT i.category,
                   COUNT(o.order_id) as order_count,
                   SUM(o.quantity) as total_quantity
            FROM orders o
            JOIN items i ON o.item_id = i.item_id
            GROUP BY i.category
            ORDER BY order_count DESC
        """
        return db_manager.execute_query(query, fetch=True)
