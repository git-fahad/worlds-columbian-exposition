"""
Base service class to eliminate code duplication
Following DRY principles
"""

from app import db
from app.models.base import BaseModel

class BaseService:
    """Base service class with common methods"""
    
    @staticmethod
    def create_model(model_class, data):
        """Generic method to create any model"""
        try:
            model = model_class(**data)
            model.save()
            return model
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_model(model, data):
        """Generic method to update any model"""
        try:
            for key, value in data.items():
                if hasattr(model, key):
                    setattr(model, key, value)
            model.save()
            return model
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_model(model):
        """Generic method to delete any model"""
        try:
            model.delete()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_model_by_id(model_class, id):
        """Generic method to get model by ID"""
        return model_class.get_by_id(id)
    
    @staticmethod
    def get_all_models(model_class):
        """Generic method to get all models"""
        return model_class.get_all()
    
    @staticmethod
    def rollback_session():
        """Rollback the current database session"""
        db.session.rollback()
