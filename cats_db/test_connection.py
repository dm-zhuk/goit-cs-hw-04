from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://dmzhuk_db_user:1rtw6pX4vl1PSbSy@cluster0.0uegaih.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(CONNECTION_STRING)
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
