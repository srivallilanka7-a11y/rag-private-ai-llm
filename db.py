from pymongo import MongoClient

MONGO_URI = "mongodb+srv://raguser:ragpassword123@cluster0.zi81umh.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["rag_db"]
collection = db["documents"]