from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI (local default)
MONGO_URI = "mongodb+srv://admin:abhi2121@cluster0.0ckpftt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Optional: Use Server API (recommended for compatibility with cloud MongoDB)
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

# Access the database
db = client["medchat_db"]

# Define collections
users_collection = db["users"]
chat_collection = db["chat_history"]
