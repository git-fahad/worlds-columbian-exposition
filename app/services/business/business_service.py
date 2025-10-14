"""
Business service for handling business-related business logic
"""

from app.services.base_service import BaseService
from app.models.business import Business

class BusinessService(BaseService):
    """Service class to handle business business logic"""
    
    @staticmethod
    def create_business(form_data):
        """Create a new business registration"""
        business_data = {
            'company_name': form_data['company_name'],
            'company_address': form_data.get('company_address'),
            'company_description': form_data.get('company_description'),
            'exhibit_type': form_data.get('exhibit_type'),
            'space_requirements': form_data.get('space_requirements', type=int),
            'exhibit_description': form_data.get('exhibit_description'),
            'contact_name': form_data['contact_name'],
            'contact_email': form_data['contact_email'],
            'contact_phone': form_data.get('contact_phone')
        }
        return BaseService.create_model(Business, business_data)
    
    @staticmethod
    def get_business_by_company_name(company_name):
        """Get business by company name"""
        return Business.get_by_company_name(company_name)
    
    @staticmethod
    def get_business_by_contact_email(email):
        """Get business by contact email"""
        return Business.get_by_contact_email(email)
    
    @staticmethod
    def get_businesses_by_exhibit_type(exhibit_type):
        """Get businesses by exhibit type"""
        return Business.get_by_exhibit_type(exhibit_type)
    
    @staticmethod
    def update_business(business_id, form_data):
        """Update business information"""
        business = Business.get_by_id(business_id)
        if not business:
            raise ValueError("Business not found")
        
        business_data = {
            'company_name': form_data.get('company_name', business.company_name),
            'company_address': form_data.get('company_address', business.company_address),
            'company_description': form_data.get('company_description', business.company_description),
            'exhibit_type': form_data.get('exhibit_type', business.exhibit_type),
            'space_requirements': form_data.get('space_requirements', type=int) or business.space_requirements,
            'exhibit_description': form_data.get('exhibit_description', business.exhibit_description),
            'contact_name': form_data.get('contact_name', business.contact_name),
            'contact_email': form_data.get('contact_email', business.contact_email),
            'contact_phone': form_data.get('contact_phone', business.contact_phone)
        }
        return BaseService.update_model(business, business_data)
