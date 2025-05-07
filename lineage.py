"""
Lineage API Routes for Atlan Integration

This module defines the API routes for lineage operations.
"""

import logging
from flask import Blueprint, request, jsonify, current_app, g
from api.auth import token_required

logger = logging.getLogger(__name__)

# Create blueprint
lineage_bp = Blueprint('lineage', __name__)

@lineage_bp.route('/', methods=['GET'])
@token_required
def get_lineage():
    """
    Get lineage for an asset
    """
    try:
        # Get query parameters
        guid = request.args.get('guid')
        direction = request.args.get('direction', 'BOTH')
        depth = request.args.get('depth', 3, type=int)
        include_process = request.args.get('includeProcess', 'true').lower() == 'true'
        
        if not guid:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing asset GUID',
                    'details': 'Asset GUID is required'
                }
            }), 400
        
        # Get lineage
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.get_lineage(
            guid=guid,
            direction=direction,
            depth=depth,
            include_process=include_process
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get lineage: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get lineage',
                'details': str(e)
            }
        }), 500

@lineage_bp.route('/', methods=['POST'])
@token_required
def create_lineage():
    """
    Create lineage between two assets
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
        
        if 'fromEntityGuid' not in data or 'toEntityGuid' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing required fields',
                    'details': 'fromEntityGuid and toEntityGuid are required'
                }
            }), 400
        
        # Extract parameters
        from_guid = data['fromEntityGuid']
        to_guid = data['toEntityGuid']
        process_guid = data.get('processGuid')
        process_name = data.get('processName')
        process_type = data.get('processType')
        
        # Create lineage
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.create_lineage(
            from_guid=from_guid,
            to_guid=to_guid,
            process_guid=process_guid,
            process_name=process_name,
            process_type=process_type
        )
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create lineage: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create lineage',
                'details': str(e)
            }
        }), 500

@lineage_bp.route('/', methods=['DELETE'])
@token_required
def delete_lineage():
    """
    Delete lineage between two assets
    """
    try:
        # Get query parameters
        from_guid = request.args.get('fromEntityGuid')
        to_guid = request.args.get('toEntityGuid')
        process_guid = request.args.get('processGuid')
        
        if not from_guid or not to_guid:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing required parameters',
                    'details': 'fromEntityGuid and toEntityGuid are required'
                }
            }), 400
        
        # Delete lineage
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.delete_lineage(
            from_guid=from_guid,
            to_guid=to_guid,
            process_guid=process_guid
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete lineage: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete lineage',
                'details': str(e)
            }
        }), 500

@lineage_bp.route('/impact', methods=['GET'])
@token_required
def get_impact_analysis():
    """
    Get impact analysis for an asset
    """
    try:
        # Get query parameters
        guid = request.args.get('guid')
        depth = request.args.get('depth', 3, type=int)
        
        if not guid:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing asset GUID',
                    'details': 'Asset GUID is required'
                }
            }), 400
        
        # Get impact analysis
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.get_impact_analysis(
            guid=guid,
            depth=depth
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get impact analysis: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get impact analysis',
                'details': str(e)
            }
        }), 500

@lineage_bp.route('/process/<process_guid>', methods=['GET'])
@token_required
def get_process_details(process_guid):
    """
    Get details for a process entity
    """
    try:
        # Get process details
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.get_process_details(process_guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get process details: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get process details',
                'details': str(e)
            }
        }), 500

@lineage_bp.route('/process/<process_guid>', methods=['PUT'])
@token_required
def update_process(process_guid):
    """
    Update a process entity
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
        
        # Update process
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.update_process(process_guid, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update process: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update process',
                'details': str(e)
            }
        }), 500

@lineage_bp.route('/graph', methods=['GET'])
@token_required
def get_lineage_graph():
    """
    Get lineage graph for visualization
    """
    try:
        # Get query parameters
        guid = request.args.get('guid')
        direction = request.args.get('direction', 'BOTH')
        depth = request.args.get('depth', 3, type=int)
        include_process = request.args.get('includeProcess', 'true').lower() == 'true'
        
        if not guid:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing asset GUID',
                    'details': 'Asset GUID is required'
                }
            }), 400
        
        # Get lineage graph
        lineage_service = current_app.config['services']['lineage']
        result = lineage_service.get_lineage_graph(
            guid=guid,
            direction=direction,
            depth=depth,
            include_process=include_process
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get lineage graph: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get lineage graph',
                'details': str(e)
            }
        }), 500
