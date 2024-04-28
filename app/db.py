# app/db.py

from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://nihaldm65:Nihal6565%40@cluster0.aszhikr.mongodb.net/"

# Initialize MongoDB client and database
client = MongoClient(MONGO_URI)
db = client["Auth2"]  # Replace "your_database_name" with your actual database name
