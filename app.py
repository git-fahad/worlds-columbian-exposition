from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/chicago_fair')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Models
class Visitor(db.Model):
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    city = db.Column(db.String(100))
    state_country = db.Column(db.String(100))
    interests = db.Column(db.ARRAY(db.String))
    notification_preference = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(100), nullable=False)
    representative_name = db.Column(db.String(255), nullable=False)
    representative_title = db.Column(db.String(100))
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50))
    pavilion_theme = db.Column(db.Text)
    pavilion_size = db.Column(db.String(50))
    technical_requirements = db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.Text)
    company_description = db.Column(db.Text)
    exhibit_type = db.Column(db.String(100))
    space_requirements = db.Column(db.Integer)
    exhibit_description = db.Column(db.Text)
    contact_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exhibits')
def exhibits():
    return render_template('exhibits.html')


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/tickets')
def tickets():
    return render_template('tickets.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Registration Routes
@app.route('/visitor-registration', methods=['GET', 'POST'])
def visitor_registration():
    if request.method == 'POST':
        try:
            visitor = Visitor(
                full_name=request.form['full_name'],
                email=request.form['email'],
                city=request.form.get('city'),
                state_country=request.form.get('state_country'),
                interests=request.form.getlist('interests'),
                notification_preference=request.form.get('notification_preference')
            )
            db.session.add(visitor)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template('visitor-registration.html')


@app.route('/country-registration', methods=['GET', 'POST'])
def country_registration():
    if request.method == 'POST':
        try:
            country = Country(
                country_name=request.form['country_name'],
                representative_name=request.form['representative_name'],
                representative_title=request.form.get('representative_title'),
                contact_email=request.form['contact_email'],
                contact_phone=request.form.get('contact_phone'),
                pavilion_theme=request.form.get('pavilion_theme'),
                pavilion_size=request.form.get('pavilion_size'),
                technical_requirements=request.form.getlist('technical_requirements')
            )
            db.session.add(country)
            db.session.commit()
            flash('Country registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template('country-registration.html')


@app.route('/business-registration', methods=['GET', 'POST'])
def business_registration():
    if request.method == 'POST':
        try:
            business = Business(
                company_name=request.form['company_name'],
                company_address=request.form.get('company_address'),
                company_description=request.form.get('company_description'),
                exhibit_type=request.form.get('exhibit_type'),
                space_requirements=request.form.get('space_requirements', type=int),
                exhibit_description=request.form.get('exhibit_description'),
                contact_name=request.form['contact_name'],
                contact_email=request.form['contact_email'],
                contact_phone=request.form.get('contact_phone')
            )
            db.session.add(business)
            db.session.commit()
            flash('Business registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template('business-registration.html')


# Initialize database
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


if __name__ == '__main__':
    app.run(debug=True)