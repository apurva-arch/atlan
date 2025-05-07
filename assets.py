"""
Asset API Routes for Atlan Integration

This module defines the API routes for asset operations.
"""

import logging
from flask import Blueprint, request, jsonify, current_app, g
from api.auth import token_required

logger = logging.getLogger(__name__)

# Create blueprint
assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/', methods=['GET'])
@token_required
def get_assets():
    """
    Get a list of assets
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort_by = request.args.get('sort')
        order = request.args.get('order')
        filter_expr = request.args.get('filter')
        
        # Get assets
        asset_service = current_app.config['services']['asset']
        result = asset_service.get_assets(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            filter_expr=filter_expr
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get assets: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get assets',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>', methods=['GET'])
@token_required
def get_asset(guid):
    """
    Get an asset by GUID
    """
    try:
        # Get asset
        asset_service = current_app.config['services']['asset']
        result = asset_service.get_asset(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get asset: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get asset',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/', methods=['POST'])
@token_required
def create_asset():
    """
    Create a new asset
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
        
        # Create asset
        asset_service = current_app.config['services']['asset']
        result = asset_service.create_asset(data)
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create asset: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create asset',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>', methods=['PUT'])
@token_required
def update_asset(guid):
    """
    Update an asset
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
        
        # Update asset
        asset_service = current_app.config['services']['asset']
        result = asset_service.update_asset(guid, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update asset: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update asset',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>', methods=['DELETE'])
@token_required
def delete_asset(guid):
    """
    Delete an asset
    """
    try:
        # Delete asset
        asset_service = current_app.config['services']['asset']
        result = asset_service.delete_asset(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete asset: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete asset',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>/classifications', methods=['POST'])
@token_required
def add_classification(guid):
    """
    Add a classification to an asset
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
        
        # Add classification
        asset_service = current_app.config['services']['asset']
        result = asset_service.add_classification(guid, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to add classification: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to add classification',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>/classifications/<classification_name>', methods=['DELETE'])
@token_required
def remove_classification(guid, classification_name):
    """
    Remove a classification from an asset
    """
    try:
        # Remove classification
        asset_service = current_app.config['services']['asset']
        result = asset_service.remove_classification(guid, classification_name)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to remove classification: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to remove classification',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>/terms', methods=['POST'])
@token_required
def add_term(guid):
    """
    Add a term to an asset
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'termGuid' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing term GUID',
                    'details': 'Term GUID is required'
                }
            }), 400
        
        # Add term
        asset_service = current_app.config['services']['asset']
        result = asset_service.add_term(guid, data['termGuid'])
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to add term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to add term',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>/terms/<term_guid>', methods=['DELETE'])
@token_required
def remove_term(guid, term_guid):
    """
    Remove a term from an asset
    """
    try:
        # Remove term
        asset_service = current_app.config['services']['asset']
        result = asset_service.remove_term(guid, term_guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to remove term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to remove term',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/<guid>/relationships', methods=['GET'])
@token_required
def get_relationships(guid):
    """
    Get relationships for an asset
    """
    try:
        # Get query parameters
        relationship_type = request.args.get('relationshipType')
        
        # Get relationships
        asset_service = current_app.config['services']['asset']
        result = asset_service.get_asset_relationships(guid, relationship_type)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get relationships: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get relationships',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/types', methods=['GET'])
@token_required
def get_asset_types():
    """
    Get all asset types
    """
    try:
        # Get asset types
        asset_service = current_app.config['services']['asset']
        result = asset_service.get_asset_types()
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get asset types: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get asset types',
                'details': str(e)
            }
        }), 500

@assets_bp.route('/types/<type_name>', methods=['GET'])
@token_required
def get_asset_schema(type_name):
    """
    Get schema for an asset type
    """
    try:
        # Get asset schema
        asset_service = current_app.config['services']['asset']
        result = asset_service.get_asset_schema(type_name)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get asset schema: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get asset schema',
                'details': str(e)
            }
        }), 500
