from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["ecommerce"]

users_collection = db["users"]


try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)