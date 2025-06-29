from pymongo import MongoClient   #lets Python talk to MongoDB
from pymongo.server_api import ServerApi  #ensures python is connected to a MongoDB server version

uri = "mongodb+srv://shorryah:mongo123@cluster0.9cfchjz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Access the database
db = client["medchat_db"]

# Define collections
users_collection = db["users"]
chat_collection = db["chat_history"]
