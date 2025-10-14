"""
Routes package - imports all route blueprints
"""

from .main import main_bp
from .registration.visitor import visitor_bp
from .registration.country import country_bp
from .registration.business import business_bp

__all__ = ['main_bp', 'visitor_bp', 'country_bp', 'business_bp']
