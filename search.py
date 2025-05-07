"""
Search API Routes for Atlan Integration

This module defines the API routes for search operations.
"""

import logging
from flask import Blueprint, request, jsonify, current_app, g
from api.auth import token_required

logger = logging.getLogger(__name__)

# Create blueprint
search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['POST'])
@token_required
def basic_search():
    """
    Perform a basic search
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing query',
                    'details': 'Query is required'
                }
            }), 400
        
        # Extract parameters
        query = data['query']
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)
        
        # Perform search
        search_service = current_app.config['services']['search']
        result = search_service.basic_search(
            query=query,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to perform basic search: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to perform basic search',
                'details': str(e)
            }
        }), 500

@search_bp.route('/advanced', methods=['POST'])
@token_required
def advanced_search():
    """
    Perform an advanced search
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing query',
                    'details': 'Query is required'
                }
            }), 400
        
        # Extract parameters
        query = data['query']
        type_names = data.get('typeName')
        classification_names = data.get('classification')
        term_guids = data.get('termGuid')
        attribute_filters = data.get('attributeFilters')
        sort_by = data.get('sortBy')
        sort_order = data.get('sortOrder')
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)
        
        # Perform search
        search_service = current_app.config['services']['search']
        result = search_service.advanced_search(
            query=query,
            type_names=type_names,
            classification_names=classification_names,
            term_guids=term_guids,
            attribute_filters=attribute_filters,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to perform advanced search: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to perform advanced search',
                'details': str(e)
            }
        }), 500

@search_bp.route('/facets', methods=['POST'])
@token_required
def faceted_search():
    """
    Perform a faceted search
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data or 'facets' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing required fields',
                    'details': 'Query and facets are required'
                }
            }), 400
        
        # Extract parameters
        query = data['query']
        facets = data['facets']
        limit = data.get('limit', 10)
        offset = data.get('offset', 0)
        
        # Perform search
        search_service = current_app.config['services']['search']
        result = search_service.faceted_search(
            query=query,
            facets=facets,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to perform faceted search: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to perform faceted search',
                'details': str(e)
            }
        }), 500

@search_bp.route('/suggest', methods=['GET'])
@token_required
def suggest():
    """
    Get search suggestions
    """
    try:
        # Get query parameters
        query = request.args.get('query')
        
        if not query:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing query',
                    'details': 'Query is required'
                }
            }), 400
        
        # Get suggestions
        search_service = current_app.config['services']['search']
        result = search_service.get_suggestions(query)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get search suggestions: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get search suggestions',
                'details': str(e)
            }
        }), 500

@search_bp.route('/recent', methods=['GET'])
@token_required
def recent_searches():
    """
    Get recent searches for the current user
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        
        # Get recent searches
        search_service = current_app.config['services']['search']
        result = search_service.get_recent_searches(
            user_id=g.user['id'],
            limit=limit
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get recent searches: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get recent searches',
                'details': str(e)
            }
        }), 500

@search_bp.route('/popular', methods=['GET'])
@token_required
def popular_searches():
    """
    Get popular searches
    """
    try:
        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        
        # Get popular searches
        search_service = current_app.config['services']['search']
        result = search_service.get_popular_searches(limit)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get popular searches: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get popular searches',
                'details': str(e)
            }
        }), 500

@search_bp.route('/saved', methods=['GET'])
@token_required
def get_saved_searches():
    """
    Get saved searches for the current user
    """
    try:
        # Get saved searches
        search_service = current_app.config['services']['search']
        result = search_service.get_saved_searches(g.user['id'])
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get saved searches: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to get saved searches',
                'details': str(e)
            }
        }), 500

@search_bp.route('/saved', methods=['POST'])
@token_required
def save_search():
    """
    Save a search
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'name' not in data or 'query' not in data:
            return jsonify({
                'error': {
                    'code': 'BAD_REQUEST',
                    'message': 'Missing required fields',
                    'details': 'Name and query are required'
                }
            }), 400
        
        # Extract parameters
        name = data['name']
        query = data['query']
        description = data.get('description')
        
        # Save search
        search_service = current_app.config['services']['search']
        result = search_service.save_search(
            user_id=g.user['id'],
            name=name,
            query=query,
            description=description
        )
        
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Failed to save search: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to save search',
                'details': str(e)
            }
        }), 500

@search_bp.route('/saved/<search_id>', methods=['DELETE'])
@token_required
def delete_saved_search(search_id):
    """
    Delete a saved search
    """
    try:
        # Delete saved search
        search_service = current_app.config['services']['search']
        result = search_service.delete_saved_search(
            user_id=g.user['id'],
            search_id=search_id
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to delete saved search: {e}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Failed to delete saved search',
                'details': str(e)
            }
        }), 500
