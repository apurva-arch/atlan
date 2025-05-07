"""
Atlan Integration Backend Application

This is the main application file that initializes the Flask application,
sets up configuration, initializes services, and registers blueprints.
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Import services
from services.auth_service import AuthService
from services.asset_service import AssetService
from services.lineage_service import LineageService
from services.glossary_service import GlossaryService
from services.search_service import SearchService
from services.admin_service import AdminService

# Import API blueprints
from api.auth import auth_bp
from api.assets import assets_bp
from api.lineage import lineage_bp
from api.glossary import glossary_bp
from api.search import search_bp
from api.admin import admin_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config=None):
    """
    Create and configure the Flask application
    
    Args:
        config (dict, optional): Configuration dictionary
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Load configuration
    app_config = {
        'ATLAN_API_URL': os.environ.get('ATLAN_API_URL', 'https://api.atlan.com'),
        'ATLAN_API_KEY': os.environ.get('ATLAN_API_KEY'),
        'ATLAN_API_SECRET': os.environ.get('ATLAN_API_SECRET'),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', 'dev-secret-key'),
        'JWT_ACCESS_TOKEN_EXPIRES': int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)),  # 1 hour
        'JWT_REFRESH_TOKEN_EXPIRES': int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 86400 * 7)),  # 7 days
    }
    
    # Override with provided config if any
    if config:
        app_config.update(config)
    
    # Set app config
    app.config.update(app_config)
    
    # Initialize services
    auth_service = AuthService(app_config)
    asset_service = AssetService(app_config, auth_service)
    lineage_service = LineageService(app_config, auth_service)
    glossary_service = GlossaryService(app_config, auth_service)
    search_service = SearchService(app_config, auth_service)
    admin_service = AdminService(app_config, auth_service)
    
    # Store services in app config for access in routes
    app.config['services'] = {
        'auth': auth_service,
        'asset': asset_service,
        'lineage': lineage_service,
        'glossary': glossary_service,
        'search': search_service,
        'admin': admin_service
    }
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(assets_bp, url_prefix='/api/assets')
    app.register_blueprint(lineage_bp, url_prefix='/api/lineage')
    app.register_blueprint(glossary_bp, url_prefix='/api/glossary')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Resource not found',
                'details': str(error)
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Internal server error',
                'details': str(error)
            }
        }), 500
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Atlan Integration API',
            'version': '1.0.0',
            'status': 'running'
        })
    
    # Health check route
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy'
        })
    
    logger.info("Application initialized")
    return app

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Create and run app
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)
