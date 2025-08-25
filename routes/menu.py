from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from models.item import Item
from routes.auth import login_required
import re

menu_bp = Blueprint('menu', __name__)

def admin_required(f):
    """Decorator to require admin access for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        # For now, allow all logged-in users to manage menu
        # In a real app, you'd check for admin role
        return f(*args, **kwargs)
    return decorated_function

@menu_bp.route('/menu')
@admin_required
def manage_menu():
    """Display menu management page"""
    try:
        # Get search parameters
        search = request.args.get('search', '').strip()
        category_filter = request.args.get('category', '').strip()
        
        if search or category_filter:
            items = Item.search_items(search, category_filter if category_filter else None)
        else:
            items = Item.get_all_items()
        
        # Get unique categories for filter dropdown
        categories = list(set([item.category for item in Item.get_all_items() if item.category]))
        categories.sort()
        
        return render_template('menu/manage_menu.html', 
                             items=items, 
                             search=search, 
                             category_filter=category_filter,
                             categories=categories)
    except Exception as e:
        flash(f'Error loading menu: {str(e)}', 'error')
        return render_template('menu/manage_menu.html', items=[], categories=[])

@menu_bp.route('/menu/add', methods=['POST'])
@admin_required
def add_item():
    """Add a new menu item"""
    try:
        data = request.get_json()
        
        # Validate input
        item_name = data.get('item_name', '').strip()
        category = data.get('category', '').strip()
        price = data.get('price')
        image_url = data.get('image_url', '').strip()
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        if not category:
            return jsonify({'error': 'Category is required'}), 400
        
        if not price or not isinstance(price, (int, float)) or price <= 0:
            return jsonify({'error': 'Valid price is required'}), 400
        
        # Validate price format
        if not re.match(r'^\d+(\.\d{1,2})?$', str(price)):
            return jsonify({'error': 'Price must be a valid number with up to 2 decimal places'}), 400
        
        # Check if item name already exists
        existing_item = Item.get_by_name(item_name)
        if existing_item:
            return jsonify({'error': 'Item with this name already exists'}), 400
        
        # Create item
        Item.create_item(item_name, category, price, image_url if image_url else None)
        
        return jsonify({'message': 'Item added successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': f'Error adding item: {str(e)}'}), 500

@menu_bp.route('/menu/edit/<int:item_id>', methods=['PUT'])
@admin_required
def edit_item(item_id):
    """Edit an existing menu item"""
    try:
        data = request.get_json()
        
        # Validate input
        item_name = data.get('item_name', '').strip()
        category = data.get('category', '').strip()
        price = data.get('price')
        image_url = data.get('image_url', '').strip()
        
        if not item_name:
            return jsonify({'error': 'Item name is required'}), 400
        
        if not category:
            return jsonify({'error': 'Category is required'}), 400
        
        if not price or not isinstance(price, (int, float)) or price <= 0:
            return jsonify({'error': 'Valid price is required'}), 400
        
        # Validate price format
        if not re.match(r'^\d+(\.\d{1,2})?$', str(price)):
            return jsonify({'error': 'Price must be a valid number with up to 2 decimal places'}), 400
        
        # Check if item exists
        existing_item = Item.get_by_id(item_id)
        if not existing_item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if new name conflicts with another item
        name_conflict = Item.get_by_name(item_name)
        if name_conflict and name_conflict.item_id != item_id:
            return jsonify({'error': 'Item with this name already exists'}), 400
        
        # Update item
        Item.update_item(item_id, item_name, category, price, image_url if image_url else None)
        
        return jsonify({'message': 'Item updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error updating item: {str(e)}'}), 500

@menu_bp.route('/menu/delete/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_item(item_id):
    """Delete a menu item"""
    try:
        # Check if item exists
        existing_item = Item.get_by_id(item_id)
        if not existing_item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Delete item
        Item.delete_item(item_id)
        
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error deleting item: {str(e)}'}), 500

@menu_bp.route('/menu/categories')
def get_categories():
    """Get all unique categories"""
    try:
        items = Item.get_all_items()
        categories = list(set([item.category for item in items if item.category]))
        categories.sort()
        return jsonify({'categories': categories})
    except Exception as e:
        return jsonify({'error': f'Error fetching categories: {str(e)}'}), 500
