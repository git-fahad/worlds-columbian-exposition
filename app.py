from app import create_app
def main():
    """Main function to run the application"""
    app = create_app()
    
    # Initialize database tables
    with app.app_context():
        from app import db
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    app.run(debug=True)

if __name__ == '__main__':
    main()