from models.database import db_manager

class Item:
    def __init__(self, item_id=None, item_name=None, category=None, price=None, image_url=None):
        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.price = price
        self.image_url = image_url
    
    @staticmethod
    def get_all_items():
        """Get all menu items"""
        query = "SELECT * FROM items ORDER BY category, item_name"
        result = db_manager.execute_query(query, fetch=True)
        
        items = []
        for row in result:
            item = Item(
                item_id=row['item_id'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price'],
                image_url=row.get('image_url')
            )
            items.append(item)
        
        return items
    
    @staticmethod
    def get_items_by_category():
        """Get items grouped by category"""
        query = "SELECT * FROM items ORDER BY category, item_name"
        result = db_manager.execute_query(query, fetch=True)
        
        items_by_category = {}
        for row in result:
            category = row['category']
            if category not in items_by_category:
                items_by_category[category] = []
            
            item = Item(
                item_id=row['item_id'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price'],
                image_url=row.get('image_url')
            )
            items_by_category[category].append(item)
        
        return items_by_category
    
    @staticmethod
    def get_by_id(item_id):
        """Get item by ID"""
        query = "SELECT * FROM items WHERE item_id = %s"
        result = db_manager.execute_query(query, (item_id,), fetch=True)
        
        if result:
            row = result[0]
            return Item(
                item_id=row['item_id'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price'],
                image_url=row.get('image_url')
            )
        return None
    
    @staticmethod
    def create_item(item_name, category, price, image_url=None):
        """Create a new menu item"""
        query = "INSERT INTO items (item_name, category, price, image_url) VALUES (%s, %s, %s, %s)"
        result = db_manager.execute_query(query, (item_name, category, price, image_url))
        return result
    
    @staticmethod
    def update_item(item_id, item_name, category, price, image_url=None):
        """Update an existing menu item"""
        query = "UPDATE items SET item_name = %s, category = %s, price = %s, image_url = %s WHERE item_id = %s"
        result = db_manager.execute_query(query, (item_name, category, price, image_url, item_id))
        return result
    
    @staticmethod
    def delete_item(item_id):
        """Delete a menu item"""
        query = "DELETE FROM items WHERE item_id = %s"
        result = db_manager.execute_query(query, (item_id,))
        return result
    
    @staticmethod
    def search_items(search_term, category_filter=None):
        """Search items by name or category"""
        if category_filter:
            query = "SELECT * FROM items WHERE (item_name LIKE %s OR category LIKE %s) AND category = %s ORDER BY category, item_name"
            params = (f'%{search_term}%', f'%{search_term}%', category_filter)
        else:
            query = "SELECT * FROM items WHERE item_name LIKE %s OR category LIKE %s ORDER BY category, item_name"
            params = (f'%{search_term}%', f'%{search_term}%')
        
        result = db_manager.execute_query(query, params, fetch=True)
        
        items = []
        for row in result:
            item = Item(
                item_id=row['item_id'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price'],
                image_url=row.get('image_url')
            )
            items.append(item)
        
        return items
    
    @staticmethod
    def get_by_name(item_name):
        """Get item by name"""
        query = "SELECT * FROM items WHERE item_name = %s"
        result = db_manager.execute_query(query, (item_name,), fetch=True)
        
        if result:
            row = result[0]
            return Item(
                item_id=row['item_id'],
                item_name=row['item_name'],
                category=row['category'],
                price=row['price'],
                image_url=row.get('image_url')
            )
        return None
