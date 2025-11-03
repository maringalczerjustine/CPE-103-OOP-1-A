# reset_db.py
import os
from app import app, db
from models import Employee, Attendance

def reset_database():
    with app.app_context():
        # Delete existing database file
        if os.path.exists('database.db'):
            os.remove('database.db')
            print("Old database deleted")
        
        # Create all tables
        db.create_all()
        print("New database created with updated schema")
        
        # Verify tables were created
        print("Database reset completed successfully!")

if __name__ == "__main__":
    reset_database()