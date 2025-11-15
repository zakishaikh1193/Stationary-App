from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
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

    # Initialize database
    from app.models.db import init_db
    init_db()
    
    return app