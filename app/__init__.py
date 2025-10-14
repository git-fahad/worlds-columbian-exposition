from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Application factory pattern"""
    import os
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/chicago_fair')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models import Visitor, Country, Business
    
    # Register blueprints
    from app.routes import main_bp, visitor_bp, country_bp, business_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(visitor_bp)
    app.register_blueprint(country_bp)
    app.register_blueprint(business_bp)
    
    return app
