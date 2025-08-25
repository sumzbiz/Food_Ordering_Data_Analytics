from flask import Blueprint, render_template, jsonify
from models.order import Order
from routes.auth import login_required

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def analytics_dashboard():
    """Analytics dashboard page"""
    try:
        # Get analytics data
        total_orders = Order.get_total_orders()
        popular_dishes = Order.get_popular_dishes(5)
        orders_per_day = Order.get_orders_per_day(7)
        orders_by_category = Order.get_orders_by_category()
        
        return render_template('analytics.html', 
                             total_orders=total_orders,
                             popular_dishes=popular_dishes,
                             orders_per_day=orders_per_day,
                             orders_by_category=orders_by_category)
    except Exception as e:
        return render_template('analytics.html', 
                             total_orders=0,
                             popular_dishes=[],
                             orders_per_day=[],
                             orders_by_category=[],
                             error=str(e))

@analytics_bp.route('/api/analytics/popular_dishes')
@login_required
def api_popular_dishes():
    """API endpoint for popular dishes data"""
    try:
        popular_dishes = Order.get_popular_dishes(5)
        return jsonify(popular_dishes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/api/analytics/orders_per_day')
@login_required
def api_orders_per_day():
    """API endpoint for orders per day data"""
    try:
        orders_per_day = Order.get_orders_per_day(7)
        return jsonify(orders_per_day)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/api/analytics/orders_by_category')
@login_required
def api_orders_by_category():
    """API endpoint for orders by category data"""
    try:
        orders_by_category = Order.get_orders_by_category()
        return jsonify(orders_by_category)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analytics_bp.route('/api/analytics/summary')
@login_required
def api_analytics_summary():
    """API endpoint for analytics summary"""
    try:
        total_orders = Order.get_total_orders()
        popular_dishes = Order.get_popular_dishes(5)
        orders_per_day = Order.get_orders_per_day(7)
        orders_by_category = Order.get_orders_by_category()
        
        summary = {
            'total_orders': total_orders,
            'popular_dishes': popular_dishes,
            'orders_per_day': orders_per_day,
            'orders_by_category': orders_by_category
        }
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
