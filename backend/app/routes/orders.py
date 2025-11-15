from flask import Blueprint, request, jsonify
from app.models import db

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/api/orders/checkout', methods=['POST'])
def checkout():
    """Process checkout and create order."""
    data = request.get_json() or {}
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        # Get cart items
        cart_items = db.get_cart_items(user_id)
        
        if not cart_items or len(cart_items) == 0:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate totals
        total_amount = sum(float(item['subtotal']) for item in cart_items)
        tax_amount = total_amount * 0.1  # 10% tax
        grand_total = total_amount + tax_amount
        
        # Create order
        order_id = db.create_order(user_id, total_amount, tax_amount, grand_total, cart_items)
        
        if not order_id:
            return jsonify({'error': 'Failed to create order'}), 500
        
        # Clear cart
        db.clear_cart(user_id)
        
        return jsonify({
            'message': 'Order placed successfully!',
            'order_id': order_id,
            'grand_total': round(grand_total, 2)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/api/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    """Get all orders for a user."""
    try:
        orders = db.get_user_orders(user_id)
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/api/orders/detail/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get detailed order information."""
    try:
        order = db.get_order_details(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({'order': order}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

