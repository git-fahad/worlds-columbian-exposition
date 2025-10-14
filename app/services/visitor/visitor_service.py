"""
Visitor service for handling visitor-related business logic
"""

from app.services.base_service import BaseService
from app.models.visitor import Visitor

class VisitorService(BaseService):
    """Service class to handle visitor business logic"""
    
    @staticmethod
    def create_visitor(form_data):
        """Create a new visitor registration"""
        visitor_data = {
            'full_name': form_data['full_name'],
            'email': form_data['email'],
            'city': form_data.get('city'),
            'state_country': form_data.get('state_country'),
            'interests': form_data.getlist('interests'),
            'notification_preference': form_data.get('notification_preference')
        }
        return BaseService.create_model(Visitor, visitor_data)
    
    @staticmethod
    def get_visitor_by_email(email):
        """Get visitor by email"""
        return Visitor.get_by_email(email)
    
    @staticmethod
    def get_visitors_by_city(city):
        """Get visitors by city"""
        return Visitor.get_by_city(city)
    
    @staticmethod
    def update_visitor(visitor_id, form_data):
        """Update visitor information"""
        visitor = Visitor.get_by_id(visitor_id)
        if not visitor:
            raise ValueError("Visitor not found")
        
        visitor_data = {
            'full_name': form_data.get('full_name', visitor.full_name),
            'email': form_data.get('email', visitor.email),
            'city': form_data.get('city', visitor.city),
            'state_country': form_data.get('state_country', visitor.state_country),
            'interests': form_data.getlist('interests') or visitor.interests,
            'notification_preference': form_data.get('notification_preference', visitor.notification_preference)
        }
        return BaseService.update_model(visitor, visitor_data)
