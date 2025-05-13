# app/routes/__init__.py

from .api import api as api_blueprint
from .web import web as web_blueprint

# Export all route blueprints
__all__ = ['api_blueprint', 'web_blueprint']

def register_routes(app):
    """Register all route blueprints with the Flask application"""
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(web_blueprint)