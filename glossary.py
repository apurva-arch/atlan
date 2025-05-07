"""
Glossary API Routes for Atlan Integration

This module defines the API routes for glossary operations.
"""

import logging
from flask import Blueprint, request, jsonify, current_app, g
from api.auth import token_required

logger = logging.getLogger(__name__)

# Create blueprint
glossary_bp = Blueprint('glossary', __name__)

@glossary_bp.route('/', methods=['GET'])
@token_required
def get_glossaries():
    """
    Get a list of glossaries
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get glossaries
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_glossaries(
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get glossaries: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get glossaries',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/<guid>', methods=['GET'])
@token_required
def get_glossary(guid):
    """
    Get a glossary by GUID
    """
    try:
        # Get glossary
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_glossary(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get glossary: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get glossary',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/', methods=['POST'])
@token_required
def create_glossary():
    """
    Create a new glossary
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
        
        # Create glossary
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.create_glossary(data)
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create glossary: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create glossary',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/<guid>', methods=['PUT'])
@token_required
def update_glossary(guid):
    """
    Update a glossary
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
        
        # Update glossary
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.update_glossary(guid, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update glossary: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update glossary',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/<guid>', methods=['DELETE'])
@token_required
def delete_glossary(guid):
    """
    Delete a glossary
    """
    try:
        # Delete glossary
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.delete_glossary(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete glossary: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete glossary',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/terms', methods=['GET'])
@token_required
def get_terms():
    """
    Get a list of terms
    """
    try:
        # Get query parameters
        glossary_guid = request.args.get('glossaryGuid')
        category_guid = request.args.get('categoryGuid')
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort_by = request.args.get('sort')
        order = request.args.get('order')
        filter_expr = request.args.get('filter')
        
        # Get terms
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_terms(
            glossary_guid=glossary_guid,
            category_guid=category_guid,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order,
            filter_expr=filter_expr
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get terms: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get terms',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/terms/<guid>', methods=['GET'])
@token_required
def get_term(guid):
    """
    Get a term by GUID
    """
    try:
        # Get term
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_term(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get term',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/terms', methods=['POST'])
@token_required
def create_term():
    """
    Create a new term
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
        
        # Create term
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.create_term(data)
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create term',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/terms/<guid>', methods=['PUT'])
@token_required
def update_term(guid):
    """
    Update a term
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
        
        # Update term
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.update_term(guid, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update term',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/terms/<guid>', methods=['DELETE'])
@token_required
def delete_term(guid):
    """
    Delete a term
    """
    try:
        # Delete term
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.delete_term(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete term',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/categories', methods=['GET'])
@token_required
def get_categories():
    """
    Get a list of categories
    """
    try:
        # Get query parameters
        glossary_guid = request.args.get('glossaryGuid')
        parent_category_guid = request.args.get('parentCategoryGuid')
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get categories
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_categories(
            glossary_guid=glossary_guid,
            parent_category_guid=parent_category_guid,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get categories: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get categories',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/categories/<guid>', methods=['GET'])
@token_required
def get_category(guid):
    """
    Get a category by GUID
    """
    try:
        # Get category
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_category(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get category: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get category',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/categories', methods=['POST'])
@token_required
def create_category():
    """
    Create a new category
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
        
        # Create category
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.create_category(data)
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to create category: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to create category',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/categories/<guid>', methods=['PUT'])
@token_required
def update_category(guid):
    """
    Update a category
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
        
        # Update category
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.update_category(guid, data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to update category: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to update category',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/categories/<guid>', methods=['DELETE'])
@token_required
def delete_category(guid):
    """
    Delete a category
    """
    try:
        # Delete category
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.delete_category(guid)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete category: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete category',
                'details': str(e)
            }
        }), 500

@glossary_bp.route('/terms/<term_guid>/assets', methods=['GET'])
@token_required
def get_assets_with_term(term_guid):
    """
    Get assets assigned to a term
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get assets with term
        glossary_service = current_app.config['services']['glossary']
        result = glossary_service.get_assets_with_term(
            term_guid=term_guid,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get assets with term: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get assets with term',
                'details': str(e)
            }
        }), 500
