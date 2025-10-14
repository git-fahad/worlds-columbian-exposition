"""
Business registration routes
"""

from flask import Blueprint
from app.routes.base_controller import BaseController
from app.services.business import BusinessService

# Create blueprint for business registration routes
business_bp = Blueprint('business', __name__)

@business_bp.route('/business-registration', methods=['GET', 'POST'])
def business_registration():
    """Business registration route"""
    return BaseController.handle_get_post_route(
        'business-registration.html',
        BusinessService.create_business,
        'Business registration successful!'
    )
