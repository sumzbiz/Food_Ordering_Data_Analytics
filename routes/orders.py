from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from models.order import Order
from models.item import Item
from routes.auth import login_required
import json

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/')
@login_required
def home():
    """Home page with menu items"""
    try:
        # Get category filter from query parameter
        category_filter = request.args.get('category', '').strip()
        
        if category_filter:
            # Filter items by category
            all_items = Item.get_all_items()
            filtered_items = [item for item in all_items if item.category == category_filter]
            
            # Group filtered items by category
            items_by_category = {}
            for item in filtered_items:
                if item.category not in items_by_category:
                    items_by_category[item.category] = []
                items_by_category[item.category].append(item)
        else:
            # Get all items grouped by category
            items_by_category = Item.get_items_by_category()
        
        # Get all categories for filter buttons
        all_items = Item.get_all_items()
        categories = list(set([item.category for item in all_items if item.category]))
        categories.sort()
        
        return render_template('home.html', 
                             items_by_category=items_by_category,
                             categories=categories,
                             selected_category=category_filter)
    except Exception as e:
        flash(f'Error loading menu: {str(e)}', 'error')
        return render_template('home.html', items_by_category={}, categories=[], selected_category='')

@orders_bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    """Place a new order"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        cart_items = data.get('cart', [])
        delivery_address = data.get('address', '').strip()
        
        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400
        
        if not delivery_address:
            return jsonify({"error": "Delivery address is required"}), 400
        
        user_id = session['user_id']
        
        # Process each item in cart
        for item in cart_items:
            item_id = item.get('item_id')
            quantity = item.get('quantity', 0)
            
            if quantity > 0:
                Order.create_order(user_id, item_id, quantity, delivery_address)
        
        return jsonify({"message": "Order placed successfully!"}), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Order placement failed: {str(e)}"}), 500

@orders_bp.route('/view_orders')
@login_required
def view_orders():
    """View all orders for the current user"""
    try:
        user_id = session['user_id']
        orders = Order.get_user_orders(user_id)
        return render_template('orders.html', orders=orders)
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'error')
        return render_template('orders.html', orders=[])

@orders_bp.route('/all_orders')
@login_required
def all_orders():
    """View all orders (admin view)"""
    try:
        orders = Order.get_all_orders()
        return render_template('all_orders.html', orders=orders)
    except Exception as e:
        flash(f'Error loading orders: {str(e)}', 'error')
        return render_template('all_orders.html', orders=[])

@orders_bp.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    """Delete an order"""
    try:
        user_id = session['user_id']
        success = Order.delete_order(order_id, user_id)
        
        if success:
            flash('Order deleted successfully!', 'success')
        else:
            flash('Order not found or you do not have permission to delete it.', 'error')
        
        return redirect(url_for('orders.view_orders'))
        
    except Exception as e:
        flash(f'Error deleting order: {str(e)}', 'error')
        return redirect(url_for('orders.view_orders'))

@orders_bp.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    """Edit an order"""
    try:
        user_id = session['user_id']
        
        if request.method == 'POST':
            quantity = request.form.get('quantity')
            delivery_address = request.form.get('delivery_address', '').strip()
            
            success = Order.update_order(order_id, user_id, quantity, delivery_address)
            
            if success:
                flash('Order updated successfully!', 'success')
                return redirect(url_for('orders.view_orders'))
            else:
                flash('Order not found or you do not have permission to edit it.', 'error')
        
        # GET request - show edit form
        orders = Order.get_user_orders(user_id)
        order_to_edit = None
        
        for order in orders:
            if order.order_id == order_id:
                order_to_edit = order
                break
        
        if not order_to_edit:
            flash('Order not found.', 'error')
            return redirect(url_for('orders.view_orders'))
        
        return render_template('edit_order.html', order=order_to_edit)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('orders.view_orders'))
    except Exception as e:
        flash(f'Error editing order: {str(e)}', 'error')
        return redirect(url_for('orders.view_orders'))

@orders_bp.route('/api/orders')
@login_required
def api_orders():
    """API endpoint to get orders for AJAX requests"""
    try:
        user_id = session['user_id']
        orders = Order.get_user_orders(user_id)
        
        # Convert orders to JSON-serializable format
        orders_data = []
        for order in orders:
            orders_data.append({
                'order_id': order.order_id,
                'item_name': order.item_name,
                'quantity': order.quantity,
                'delivery_address': order.delivery_address,
                'order_timestamp': order.order_timestamp.strftime('%Y-%m-%d %H:%M:%S') if order.order_timestamp else None,
                'category': order.category,
                'price': float(order.price) if order.price else 0
            })
        
        return jsonify(orders_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
