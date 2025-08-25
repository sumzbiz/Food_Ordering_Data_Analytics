from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from config import Config
from routes.auth import auth_bp
from routes.orders import orders_bp
from routes.analytics import analytics_bp
from routes.menu import menu_bp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    
    # Root route - redirect to orders home
    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('orders.home'))
        return redirect(url_for('auth.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
