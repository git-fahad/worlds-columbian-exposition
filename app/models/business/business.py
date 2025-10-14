"""
Business model for the World's Columbian Exposition
"""

from app.models.base import BaseModel
from app import db

class Business(BaseModel):
    """Business model for the World's Columbian Exposition"""
    __tablename__ = 'businesses'
    
    company_name = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.Text)
    company_description = db.Column(db.Text)
    exhibit_type = db.Column(db.String(100))
    space_requirements = db.Column(db.Integer)
    exhibit_description = db.Column(db.Text)
    contact_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50))
    
    def to_dict(self):
        """Convert business to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'company_name': self.company_name,
            'company_address': self.company_address,
            'company_description': self.company_description,
            'exhibit_type': self.exhibit_type,
            'space_requirements': self.space_requirements,
            'exhibit_description': self.exhibit_description,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone
        })
        return base_dict
    
    @classmethod
    def get_by_company_name(cls, company_name):
        """Get business by company name"""
        return cls.query.filter_by(company_name=company_name).first()
    
    @classmethod
    def get_by_contact_email(cls, email):
        """Get business by contact email"""
        return cls.query.filter_by(contact_email=email).first()
    
    @classmethod
    def get_by_exhibit_type(cls, exhibit_type):
        """Get businesses by exhibit type"""
        return cls.query.filter_by(exhibit_type=exhibit_type).all()
    
    def __repr__(self):
        return f'<Business {self.company_name}>'
