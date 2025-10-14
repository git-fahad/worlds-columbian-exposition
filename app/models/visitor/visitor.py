"""
Visitor model for the World's Columbian Exposition
"""

from app.models.base import BaseModel
from app import db

class Visitor(BaseModel):
    """Visitor model for the World's Columbian Exposition"""
    __tablename__ = 'visitors'
    
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    city = db.Column(db.String(100))
    state_country = db.Column(db.String(100))
    interests = db.Column(db.ARRAY(db.String))
    notification_preference = db.Column(db.String(50))
    
    def to_dict(self):
        """Convert visitor to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'full_name': self.full_name,
            'email': self.email,
            'city': self.city,
            'state_country': self.state_country,
            'interests': self.interests,
            'notification_preference': self.notification_preference
        })
        return base_dict
    
    @classmethod
    def get_by_email(cls, email):
        """Get visitor by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_city(cls, city):
        """Get visitors by city"""
        return cls.query.filter_by(city=city).all()
    
    def __repr__(self):
        return f'<Visitor {self.full_name}>'
