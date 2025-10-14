"""
Base model class to eliminate code duplication
Following DRY principles
"""

from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base model class with common fields and methods"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary - to be overridden by subclasses"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def save(self):
        """Save the model to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete the model from database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def get_by_id(cls, id):
        """Get model by ID"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all models"""
        return cls.query.all()
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
