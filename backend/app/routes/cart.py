from flask import Blueprint, request, jsonify
from app.models import db

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """Get all cart items for a user."""
    try:
        items = db.get_cart_items(user_id)
        total = sum(float(item['subtotal']) for item in items)
        return jsonify({
            'cart_items': items,
            'total': round(total, 2),
            'item_count': len(items)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/api/cart', methods=['POST'])
def add_to_cart():
    """Add an item to cart."""
    data = request.get_json() or {}
    
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Validation
    if not user_id or not product_id:
        return jsonify({'error': 'user_id and product_id are required'}), 400
    
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity'}), 400
    
    # Check if product exists and has enough stock
    product = db.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if product['stock'] < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    try:
        success = db.add_to_cart(user_id, product_id, quantity)
        if not success:
            return jsonify({'error': 'Failed to add item to cart'}), 500
        return jsonify({'message': 'Item added to cart successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/api/cart/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    """Update quantity of a cart item."""
    data = request.get_json() or {}
    quantity = data.get('quantity')
    
    if quantity is None:
        return jsonify({'error': 'Quantity is required'}), 400
    
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity'}), 400
    
    try:
        success = db.update_cart_quantity(cart_item_id, quantity)
        if not success:
            return jsonify({'error': 'Cart item not found'}), 404
        
        message = 'Cart item removed' if quantity <= 0 else 'Cart item updated successfully'
        return jsonify({'message': message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/api/cart/<int:cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    """Remove an item from cart."""
    try:
        success = db.remove_from_cart(cart_item_id)
        if not success:
            return jsonify({'error': 'Cart item not found'}), 404
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/api/cart/clear/<int:user_id>', methods=['POST'])
def clear_cart(user_id):
    """Clear all items from user's cart."""
    try:
        db.clear_cart(user_id)
        return jsonify({'message': 'Cart cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

