from flask import Blueprint, request, jsonify
from app.models import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('fullName') or data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    # Basic validation
    if not username or not email or not password:
        return jsonify({'error': 'username, email and password are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'password must be at least 6 characters long'}), 400

    # Check if user exists
    existing = db.get_user_by_email(email)
    if existing:
        return jsonify({'error': 'email already registered'}), 409

    user_id = db.create_user(username, email, password, phone)
    if not user_id:
        return jsonify({'error': 'could not create user'}), 500

    return jsonify({'message': 'user created', 'user_id': user_id}), 201
