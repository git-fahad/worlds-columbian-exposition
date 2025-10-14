"""
Country service for handling country-related business logic
"""

from app.services.base_service import BaseService
from app.models.country import Country

class CountryService(BaseService):
    """Service class to handle country business logic"""
    
    @staticmethod
    def create_country(form_data):
        """Create a new country registration"""
        country_data = {
            'country_name': form_data['country_name'],
            'representative_name': form_data['representative_name'],
            'representative_title': form_data.get('representative_title'),
            'contact_email': form_data['contact_email'],
            'contact_phone': form_data.get('contact_phone'),
            'pavilion_theme': form_data.get('pavilion_theme'),
            'pavilion_size': form_data.get('pavilion_size'),
            'technical_requirements': form_data.getlist('technical_requirements')
        }
        return BaseService.create_model(Country, country_data)
    
    @staticmethod
    def get_country_by_name(country_name):
        """Get country by name"""
        return Country.get_by_country_name(country_name)
    
    @staticmethod
    def get_country_by_email(email):
        """Get country by representative email"""
        return Country.get_by_representative_email(email)
    
    @staticmethod
    def update_country(country_id, form_data):
        """Update country information"""
        country = Country.get_by_id(country_id)
        if not country:
            raise ValueError("Country not found")
        
        country_data = {
            'country_name': form_data.get('country_name', country.country_name),
            'representative_name': form_data.get('representative_name', country.representative_name),
            'representative_title': form_data.get('representative_title', country.representative_title),
            'contact_email': form_data.get('contact_email', country.contact_email),
            'contact_phone': form_data.get('contact_phone', country.contact_phone),
            'pavilion_theme': form_data.get('pavilion_theme', country.pavilion_theme),
            'pavilion_size': form_data.get('pavilion_size', country.pavilion_size),
            'technical_requirements': form_data.getlist('technical_requirements') or country.technical_requirements
        }
        return BaseService.update_model(country, country_data)
