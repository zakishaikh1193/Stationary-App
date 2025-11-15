from flask import Blueprint, request, jsonify
from app.models import db

products_bp = Blueprint('products', __name__)


@products_bp.route('/api/products', methods=['GET'])
def get_products():
    """Get all products."""
    try:
        products = db.get_all_products()
        return jsonify({'products': products}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    try:
        product = db.get_product_by_id(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'product': product}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product."""
    data = request.get_json() or {}
    
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    category = data.get('category', '')
    image_url = data.get('image_url', '')
    stock = data.get('stock', 0)
    
    # Validation
    if not name or price is None:
        return jsonify({'error': 'Name and price are required'}), 400
    
    try:
        price = float(price)
        stock = int(stock)
        if price < 0 or stock < 0:
            return jsonify({'error': 'Price and stock must be non-negative'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid price or stock value'}), 400
    
    try:
        product_id = db.create_product(name, description, price, category, image_url, stock)
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    data = request.get_json() or {}
    
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    category = data.get('category', '')
    image_url = data.get('image_url', '')
    stock = data.get('stock', 0)
    
    # Validation
    if not name or price is None:
        return jsonify({'error': 'Name and price are required'}), 400
    
    try:
        price = float(price)
        stock = int(stock)
        if price < 0 or stock < 0:
            return jsonify({'error': 'Price and stock must be non-negative'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid price or stock value'}), 400
    
    try:
        success = db.update_product(product_id, name, description, price, category, image_url, stock)
        if not success:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product."""
    try:
        success = db.delete_product(product_id)
        if not success:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

