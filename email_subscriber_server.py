import pymongo
from dotenv import load_dotenv
import os
from flask import Flask, request
load_dotenv()
from flask_cors import CORS


MONGO_USER = os.getenv("MONGO_DB_USER")
MONGO_PASSWORD = os.getenv("MONGO_PWD")


client = pymongo.MongoClient("mongodb+srv://"+ MONGO_USER +":"+ MONGO_PASSWORD +"@email.p9az5.mongodb.net/?retryWrites=true&w=majority")
db = client.Courses
collection = db.RobloxCourseSubs

server = Flask(__name__)
CORS(server)

def add_subscriber(email):
    try:
        # check if the email key exists in the database if not create a new list of emails
        if collection.count_documents({"_id": "emails"}) == 0:
            collection.insert_one({"_id": "emails", "emails": [email]})
        else:
            # add the email to the list of emails
            collection.update_one({"_id": "emails"}, {"$push": {"emails": email}})
        return True
    except:
        return False

@server.route("/", methods=["GET"])
def index():
    return "Hello World"

@server.route("/add_subscriber", methods=["POST"])
def add_subscriber_route():
    print("in the function")
    data = request.json
    email = data["email"]
    print(data)
    if add_subscriber(email):
        # return json success message
        return {"success": True}
    else:
        return {"success": False}

if __name__ == "__main__":
    server.run()