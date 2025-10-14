"""
Visitor registration routes
"""

from flask import Blueprint
from app.routes.base_controller import BaseController
from app.services.visitor import VisitorService

# Create blueprint for visitor registration routes
visitor_bp = Blueprint('visitor', __name__)

@visitor_bp.route('/visitor-registration', methods=['GET', 'POST'])
def visitor_registration():
    """Visitor registration route"""
    return BaseController.handle_get_post_route(
        'visitor-registration.html',
        VisitorService.create_visitor,
        'Registration successful!'
    )
