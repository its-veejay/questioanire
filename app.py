from flask import Flask, jsonify, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    return '<h1>Hello {}, you are on a Home Page.</h1>'.format(name)

################################## Mongo CRUD Operations ######################
try:
    #mongo = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000) #connecting to mongo server
    mongo = pymongo.MongoClient("mongodb+srv://nishadatascientist12:L0DRVxKQeexcOF56@appcluster.n8hsla5.mongodb.net/?retryWrites=true&w=majority") #connecting to mongo server
    db = mongo.Questionaire #creating a new database namely company
    mongo.server_info()
except:
    print("Error while connecting database!")

##################################
@app.route("/questions",methods=["GET"])
def get_all_questions(): #function to display all the  questions from database
    try:
        data = list(db.Questions.find())        
        for question in data:
            question["_id"] = str(question["_id"])
        return Response(response=json.dumps(data),status=200,mimetype="application/json")
    except Exception as ex: #except block used in case any error occures while connecting with database or any other unexpected error occurs
        print(ex)
        return Response(response=json.dumps({"message":"Cannot read questions",}),status=500,mimetype="application/json")
##################################

@app.route("/questions/keywords",methods=["GET"])
def get_question(keywords): #function to get question with specific keyword from database
    try:
        data = list(db.question)
        # data = list(db.question.find({"cuisine" : { "$regex" : "^C" }})
        print(data)
        print("new")
        keywords = request.args.get('keywords', '').split(',')
        print(keywords)
        query = {'$or': [{'field1' : {'$regex' : keywords, '$options' : 'i'}}for keyword in keywords]}
        data = list(data.find(query))
        
        return Response(response=json.dumps(data),status=200,mimetype="application/json")
        # for user in data:
        #     user["_id"]=str(user["_id"])    
        
        # keywords = request.args.get('keywords', '').split(',')
        # query = {'$or': [{'field1' : {'$regex' : keyword, '$options' : 'i'}}for keyword in keywords]}
        # data = list(collection.find(query))
        # return jsonify(data)

    except Exception as ex: #except block used in case wrong user id is given or any other unexpected error occurs
        print(ex)
        return Response(response=json.dumps({"message": "Error Cannot Find question"}),status=500,mimetype="application/json")
    
##################################
@app.route("/question",methods=["POST"])
def create_Question(): #function to create new user in database
    try:
        user={"name": request.form["name"],"email": request.form["email"],"password": request.form["password"]}
        dbResponse=db.users.insert_one(user)
        data=list(db.users.find({"_id": ObjectId(dbResponse.inserted_id)}))
        for user in data:
            user["_id"]=str(user["_id"])
        return Response(response=json.dumps({"message":"User created","id": f"{dbResponse.inserted_id}","name": data[0]["name"],"email": data[0]["email"],"password": data[0]["password"]}),status=200,mimetype="application/json")
    except Exception as ex: #except block used in case any error occur while adding data or any wrong entry is filled or any entry filled with wrong or improper data or any other unexpected error occurs
        print(ex)
        
##################################
@app.route("/users/<id>",methods=["PATCH"])
def update_user(id): #function to update the data of user with specific id in database
    try:
        dbResponse=db.users.update_one({"_id": ObjectId(id)},{"$set": {"name": request.form["name"],"email": request.form["email"],"password": request.form["password"]}})
        if dbResponse.modified_count==1:
            return Response(response=json.dumps({"message": "user updated"}),status=200,mimetype="application/json")
        else:
            return Response(response=json.dumps({"message": "nothing to modify"}),status=200,mimetype="application/json")
    except Exception as ex: #excep block ised in case wrong id is used or user with the id is not present or any other unexpected error occurs
        print(ex)
        return Response(response=json.dumps({"message": "Error Cannot update"}),status=500,mimetype="application/json")

##################################  
@app.route("/users/<id>",methods=["DELETE"])
def delete_user(id): #fucntion to delete user from database 
    try:
        data=list(db.users.find({"_id": ObjectId(id)}))
        for user in data:
            user["_id"]=str(user["_id"])
        dbResponse=db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count==1:
            return Response(response=json.dumps({"message": "User Deleted Successfully ","id": id,"name": data[0]["name"],"email": data[0]["email"],"password": data[0]["password"]}),status=200,mimetype="application/json")
        else:
            return Response(response=json.dumps({"message": "User not found"}),status=500,mimetype="application/json")
    except Exception as ex: #except block if user not found or any other unexpected error occurs
        print("*********************")
        print(ex)
        print("*********************")
        return Response(response=json.dumps({"message": "Cannot delete user"}),status=500,mimetype="application/json")
################################## 


if __name__ == "__main__":
    app.run(debug=True)