from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db_manager
import re

class User:
    def __init__(self, user_id=None, username=None, password_hash=None, created_at=None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if not username or len(username) < 3 or len(username) > 50:
            return False, "Username must be between 3 and 50 characters"
        
        # Check for alphanumeric and underscore only
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        return True, ""
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create_user(username, password):
        """Create a new user"""
        # Validate input
        valid_username, username_error = User.validate_username(username)
        if not valid_username:
            raise ValueError(username_error)
        
        valid_password, password_error = User.validate_password(password)
        if not valid_password:
            raise ValueError(password_error)
        
        # Check if username already exists
        existing_user = User.get_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        # Create user
        user = User(username=username)
        user.set_password(password)
        
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        db_manager.execute_query(query, (username, user.password_hash))
        
        return user
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        query = "SELECT * FROM users WHERE username = %s"
        result = db_manager.execute_query(query, (username,), fetch=True)
        
        if result:
            user_data = result[0]
            return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                created_at=user_data['created_at']
            )
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = %s"
        result = db_manager.execute_query(query, (user_id,), fetch=True)
        
        if result:
            user_data = result[0]
            return User(
                user_id=user_data['user_id'],
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                created_at=user_data['created_at']
            )
        return None
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user with username and password"""
        user = User.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None
