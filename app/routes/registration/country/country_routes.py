"""
Country registration routes
"""

from flask import Blueprint
from app.routes.base_controller import BaseController
from app.services.country import CountryService

# Create blueprint for country registration routes
country_bp = Blueprint('country', __name__)

@country_bp.route('/country-registration', methods=['GET', 'POST'])
def country_registration():
    """Country registration route"""
    return BaseController.handle_get_post_route(
        'country-registration.html',
        CountryService.create_country,
        'Country registration successful!'
    )
