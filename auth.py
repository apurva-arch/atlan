"""
Authentication API Routes for Atlan Integration

This module defines the API routes for authentication operations.
"""

import logging
from flask import Blueprint, request, jsonify, current_app, g
import jwt
from functools import wraps

logger = logging.getLogger(__name__)

# Create blueprint
auth_bp = Blueprint('auth', __name__)

def token_required(f):
    """
    Decorator to require a valid token for API routes
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Token is missing',
                    'details': 'Authentication token is required'
                }
            }), 401
        
        try:
            # Verify token
            auth_service = current_app.config['services']['auth']
            if not auth_service.validate_token(token):
                raise Exception("Invalid token")
            
            # Get user info
            user_info = auth_service.get_user_info(token)
            g.user = user_info
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Invalid token',
                    'details': str(e)
                }
            }), 401
    
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return a token
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing credentials',
                    'details': 'Username and password are required'
                }
            }), 400
        
        username = data['username']
        password = data['password']
        
        # Authenticate user
        auth_service = current_app.config['services']['auth']
        result = auth_service.authenticate_user(username, password)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return jsonify({
            'error': {
                'code': 'AUTHENTICATION_FAILED',
                'message': 'Authentication failed',
                'details': str(e)
            }
        }), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh an access token using a refresh token
    """
    try:
        data = request.get_json()
        
        if not data or 'refresh_token' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing refresh token',
                    'details': 'Refresh token is required'
                }
            }), 400
        
        refresh_token = data['refresh_token']
        
        # Refresh token
        auth_service = current_app.config['services']['auth']
        result = auth_service.refresh_token(refresh_token)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        return jsonify({
            'error': {
                'code': 'REFRESH_FAILED',
                'message': 'Token refresh failed',
                'details': str(e)
            }
        }), 401

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_user_info():
    """
    Get information about the authenticated user
    """
    try:
        return jsonify(g.user), 200
    except Exception as e:
        logger.error(f"Failed to get user info: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get user info',
                'details': str(e)
            }
        }), 500

@auth_bp.route('/validate', methods=['POST'])
def validate_token():
    """
    Validate a token
    """
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing token',
                    'details': 'Token is required'
                }
            }), 400
        
        token = data['token']
        
        # Validate token
        auth_service = current_app.config['services']['auth']
        is_valid = auth_service.validate_token(token)
        
        return jsonify({
            'valid': is_valid
        }), 200
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        return jsonify({
            'error': {
                'code': 'VALIDATION_FAILED',
                'message': 'Token validation failed',
                'details': str(e)
            }
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout a user (invalidate token)
    """
    # Note: In a real implementation, you would invalidate the token
    # This is a placeholder implementation
    return jsonify({
        'message': 'Logout successful'
    }), 200
