from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/api', methods=['GET'])
def api_root():
    """API root endpoint - health check."""
    return jsonify({
        'status': 'ok',
        'message': 'Stationary App API is running',
        'version': '1.0.0'
    }), 200

@main_bp.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'API is healthy'
    }), 200

@main_bp.route('/api/items', methods=['GET'])
def get_items():
    # This is just a sample response - you can modify based on your needs
    items = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"}
    ]
    return jsonify(items)

@main_bp.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Sample single item response
    item = {"id": item_id, "name": f"Item {item_id}"}
    return jsonify(item)