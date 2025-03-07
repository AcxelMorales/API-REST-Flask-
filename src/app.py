from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost/pythonreactdb"

mongoDB = PyMongo(app)
CORS(app)

db = mongoDB.db.users


@app.route("/users", methods=["POST"])
def createdUser():
    id = db.insert({
        "name": request.json["name"],
        "email": request.json["email"],
        "password": request.json["password"]
    })

    return jsonify({
        "ok": True,
        "id": str(ObjectId(id)),
        "message": "User created"
    })


@app.route("/users", methods=["GET"])
def getUsers():
    users = []

    for doc in db.find():
        users.append({
            "_id": str(ObjectId(doc["_id"])),
            "name": doc["name"],
            "email": doc["email"]
        })

    return jsonify({
        "ok": True,
        "users": users
    })


@app.route("/user/<id>", methods=["GET"])
def getUser(id):
    user = db.find_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "ok": True,
        "_id": str(ObjectId(user["_id"])),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    })


@app.route("/user/<id>", methods=["DELETE"])
def deleteUser(id):
    db.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "ok": True,
        "message": "User deleted"
    })


@app.route("/user/<id>", methods=["PUT"])
def updateUser(id):
    db.update({
        "_id": ObjectId(id)
    }, {
        "$set": {
            "name": request.json["name"],
            "email": request.json["email"],
            "password": request.json["password"]
        }
    })

    return jsonify({
        "ok": True,
        "message": "User updated"
    })


if __name__ == "__main__":
    app.run(debug=True)
