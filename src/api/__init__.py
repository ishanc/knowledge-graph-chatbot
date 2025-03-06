from flask import Flask
from .routes import api

def create_app(config=None):
    app = Flask(__name__)
    
    # Load configuration
    if config:
        app.config.update(config)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app