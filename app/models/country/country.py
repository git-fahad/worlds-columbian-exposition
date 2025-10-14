"""
Country model for the World's Columbian Exposition
"""

from app.models.base import BaseModel
from app import db

class Country(BaseModel):
    """Country model for the World's Columbian Exposition"""
    __tablename__ = 'countries'
    
    country_name = db.Column(db.String(100), nullable=False)
    representative_name = db.Column(db.String(255), nullable=False)
    representative_title = db.Column(db.String(100))
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50))
    pavilion_theme = db.Column(db.Text)
    pavilion_size = db.Column(db.String(50))
    technical_requirements = db.Column(db.ARRAY(db.String))
    
    def to_dict(self):
        """Convert country to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'country_name': self.country_name,
            'representative_name': self.representative_name,
            'representative_title': self.representative_title,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'pavilion_theme': self.pavilion_theme,
            'pavilion_size': self.pavilion_size,
            'technical_requirements': self.technical_requirements
        })
        return base_dict
    
    @classmethod
    def get_by_country_name(cls, country_name):
        """Get country by name"""
        return cls.query.filter_by(country_name=country_name).first()
    
    @classmethod
    def get_by_representative_email(cls, email):
        """Get country by representative email"""
        return cls.query.filter_by(contact_email=email).first()
    
    def __repr__(self):
        return f'<Country {self.country_name}>'
