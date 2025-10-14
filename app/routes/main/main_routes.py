"""
Main routes for the World's Columbian Exposition
"""

from flask import Blueprint
from app.routes.base_controller import BaseController

# Create blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route"""
    return BaseController.render_page('index.html')

@main_bp.route('/exhibits')
def exhibits():
    """Exhibits page route"""
    return BaseController.render_page('exhibits.html')

@main_bp.route('/events')
def events():
    """Events page route"""
    return BaseController.render_page('events.html')

@main_bp.route('/tickets')
def tickets():
    """Tickets page route"""
    return BaseController.render_page('tickets.html')

@main_bp.route('/about')
def about():
    """About page route"""
    return BaseController.render_page('about.html')
