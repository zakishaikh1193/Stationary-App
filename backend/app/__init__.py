from flask import Flask
from flask_cors import CORS
from config import Config
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    try:
        from app.routes.main import main_bp
        app.register_blueprint(main_bp)

        # Register auth blueprint
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp)

        # Register products blueprint
        from app.routes.products import products_bp
        app.register_blueprint(products_bp)

        # Register cart blueprint
        from app.routes.cart import cart_bp
        app.register_blueprint(cart_bp)

        # Register orders blueprint
        from app.routes.orders import orders_bp
        app.register_blueprint(orders_bp)
        
        app.logger.info("All blueprints registered successfully")
    except Exception as e:
        app.logger.error(f"Error registering blueprints: {e}")
        raise

    # Initialize database (with error handling)
    try:
        from app.models.db import init_db
        init_db()
        app.logger.info("Database initialized successfully")
    except Exception as e:
        app.logger.error(f"Error initializing database: {e}")
        # Don't raise - allow app to start even if DB init fails
        # Routes will handle DB errors gracefully
    
    return app