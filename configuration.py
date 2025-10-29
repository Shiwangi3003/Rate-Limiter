
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os 

load_dotenv()

uri = os.getenv("MONGODB_URL")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.rates_db
collection = db.rates_db

