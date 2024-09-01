from app import db
from models import User

# Create the database and the tables
db.create_all()

print("Database and tables created successfully!")
