"""
Admin API Routes for Atlan Integration

This module defines the API routes for administrative operations.
"""

import logging
from flask import Blueprint, request, jsonify, current_app, g
from api.auth import token_required

logger = logging.getLogger(__name__)

# Create blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    """
    Get a list of users
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort_by = request.args.get('sort')
        order = request.args.get('order')
        filter_expr = request.args.get('filter')
        
        # Get users
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_users(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            filter_expr=filter_expr
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get users',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """
    Get a user by ID
    """
    try:
        # Get user
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_user(user_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get user: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get user',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/users', methods=['POST'])
@token_required
def create_user():
    """
    Create a new user
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing request body',
                    'details': 'Request body is required'
                }
            }), 400
        
        # Create user
        admin_service = current_app.config['services']['admin']
        result = admin_service.create_user(data)
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create user',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/users/<user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """
    Update a user
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing request body',
                    'details': 'Request body is required'
                }
            }), 400
        
        # Update user
        admin_service = current_app.config['services']['admin']
        result = admin_service.update_user(user_id, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update user',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """
    Delete a user
    """
    try:
        # Delete user
        admin_service = current_app.config['services']['admin']
        result = admin_service.delete_user(user_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete user: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete user',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups', methods=['GET'])
@token_required
def get_groups():
    """
    Get a list of groups
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get groups
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_groups(
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get groups: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get groups',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups/<group_id>', methods=['GET'])
@token_required
def get_group(group_id):
    """
    Get a group by ID
    """
    try:
        # Get group
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_group(group_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get group: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get group',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups', methods=['POST'])
@token_required
def create_group():
    """
    Create a new group
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing request body',
                    'details': 'Request body is required'
                }
            }), 400
        
        # Create group
        admin_service = current_app.config['services']['admin']
        result = admin_service.create_group(data)
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create group: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create group',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups/<group_id>', methods=['PUT'])
@token_required
def update_group(group_id):
    """
    Update a group
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing request body',
                    'details': 'Request body is required'
                }
            }), 400
        
        # Update group
        admin_service = current_app.config['services']['admin']
        result = admin_service.update_group(group_id, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update group: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update group',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups/<group_id>', methods=['DELETE'])
@token_required
def delete_group(group_id):
    """
    Delete a group
    """
    try:
        # Delete group
        admin_service = current_app.config['services']['admin']
        result = admin_service.delete_group(group_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete group: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete group',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups/<group_id>/users/<user_id>', methods=['POST'])
@token_required
def add_user_to_group(group_id, user_id):
    """
    Add a user to a group
    """
    try:
        # Add user to group
        admin_service = current_app.config['services']['admin']
        result = admin_service.add_user_to_group(user_id, group_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to add user to group: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to add user to group',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/groups/<group_id>/users/<user_id>', methods=['DELETE'])
@token_required
def remove_user_from_group(group_id, user_id):
    """
    Remove a user from a group
    """
    try:
        # Remove user from group
        admin_service = current_app.config['services']['admin']
        result = admin_service.remove_user_from_group(user_id, group_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to remove user from group: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to remove user from group',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/config', methods=['GET'])
@token_required
def get_workspace_config():
    """
    Get workspace configuration
    """
    try:
        # Get workspace configuration
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_workspace_config()
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get workspace configuration: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get workspace configuration',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/config', methods=['PUT'])
@token_required
def update_workspace_config():
    """
    Update workspace configuration
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing request body',
                    'details': 'Request body is required'
                }
            }), 400
        
        # Update workspace configuration
        admin_service = current_app.config['services']['admin']
        result = admin_service.update_workspace_config(data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update workspace configuration: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update workspace configuration',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/audit', methods=['GET'])
@token_required
def get_audit_logs():
    """
    Get audit logs
    """
    try:
        # Get query parameters
        start_time = request.args.get('startTime', type=int)
        end_time = request.args.get('endTime', type=int)
        user_id = request.args.get('userId')
        action = request.args.get('action')
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get audit logs
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_audit_logs(
            start_time=start_time,
            end_time=end_time,
            user_id=user_id,
            action=action,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get audit logs: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get audit logs',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/metrics', methods=['GET'])
@token_required
def get_usage_metrics():
    """
    Get usage metrics
    """
    try:
        # Get query parameters
        start_time = request.args.get('startTime', type=int)
        end_time = request.args.get('endTime', type=int)
        metric_type = request.args.get('type')
        
        # Get usage metrics
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_usage_metrics(
            start_time=start_time,
            end_time=end_time,
            metric_type=metric_type
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get usage metrics: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get usage metrics',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/apikeys', methods=['GET'])
@token_required
def get_api_keys():
    """
    Get API keys
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get API keys
        admin_service = current_app.config['services']['admin']
        result = admin_service.get_api_keys(
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get API keys: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get API keys',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/apikeys', methods=['POST'])
@token_required
def create_api_key():
    """
    Create a new API key
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing name',
                    'details': 'Name is required'
                }
            }), 400
        
        # Extract parameters
        name = data['name']
        description = data.get('description')
        expiry = data.get('expiry')
        
        # Create API key
        admin_service = current_app.config['services']['admin']
        result = admin_service.create_api_key(
            name=name,
            description=description,
            expiry=expiry
        )
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create API key: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create API key',
                'details': str(e)
            }
        }), 500

@admin_bp.route('/apikeys/<key_id>', methods=['DELETE'])
@token_required
def delete_api_key(key_id):
    """
    Delete an API key
    """
    try:
        # Delete API key
        admin_service = current_app.config['services']['admin']
        result = admin_service.delete_api_key(key_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete API key: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete API key',
                'details': str(e)
            }
        }), 500
