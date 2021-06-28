"""
Registration of a user 
Each user gets 10 tokens
Store a sentence our database for 1 token
Retireve his stored sentense on our database for 1 token

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")  
# where db is the name of service specified in docker compose file
# 27017 is the default port used by mongodb
db = client.SentencesDatabase
users = db["Users"] #name of collection

def verifyPW(username, password):
    hashedPW = users.find({
        "Username" : username   #criteria
    })[0]["Password"]
    
    if bcrypt.hashpw(password.encode("utf8"), hashedPW) == hashedPW:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username" : username
    })[0]["Tokens"]
    
    return tokens

class Register(Resource):
    def post(self):
        #Get posted data by the user
        postedData = request.get_json()
        
        #Get the data
        username = postedData["username"]
        password = postedData["password"]
        
        #hash(password + salt)
        
        hashedPW = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        starterTokens = 10
        
        #Store username and password into the database
        users.insert({
            "Username" : username,
            "Password" : hashedPW,
            "Sentence" : "" ,
            "Tokens" : starterTokens
        })
        
        retJson = {
            "status" : 200 ,
            "msg" : "You have successfully signed up for the API",
            "Tokens remaining" :  starterTokens

        }
        return jsonify(retJson)
        
class Store(Resource):
    def post(self):
        #Get posted data by the user
        postedData = request.get_json()
        
        #Read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        
        #Verify the username and password match
        correctPW = verifyPW(username, password) 
        
        if not correctPW:
            retJson = {
                "status" : 302 ,
                "msg" : "Incorrect Password"
            }
            return jsonify(retJson)
        #Verify user has enough tokens
        numOfTokens = countTokens(username) 
        
        if numOfTokens <= 0:
            retJson = {
                "status" : 303 ,
                "msg" : "Not enough Tokens"
            }
            return jsonify(retJson)
        #Store the sentence and return 200 ok
        users.update({
            "Username" : username
            }, {
                "$set" : {
                    "Sentence" : sentence ,
                    "Tokens" : numOfTokens-1
                    }
            })
        
        retJson = {
            "status" : 200 ,
            "msg" : "Sentence saved successfully" ,
            "Tokens remaining" :  numOfTokens

        }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
        #Get posted data by the user
        postedData = request.get_json()
        
        #Read the data
        username = postedData["username"]
        password = postedData["password"]
        
        #Verify the username and password match
        correctPW = verifyPW(username, password) 
        
        if not correctPW:
            retJson = {
                "status" : 302 ,
                "msg" : "Incorrect Password"
            }
            return jsonify(retJson)
        #Verify user has enough tokens
        numOfTokens = countTokens(username) 
        
        if numOfTokens <= 0:
            retJson = {
                "status" : 303 ,
                "msg" : "Not enough Tokens"
            }
            return jsonify(retJson)
        
        users.update({
            "Username" : username,  # criteria
        }, {
            "$set" : {
                "Tokens": numOfTokens-1
            }
        })
        
        sentence = users.find({
            "Username" : username
        })[0]["Sentence"]
        
        retJson = {
            "status" : 200 ,
            "msg" : sentence , 
            "Tokens remaining" :  numOfTokens
        }
        return jsonify(retJson)
        


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")



@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)







    
# in folder say `export FLASK_APP=app.py`
# then `flask run`

# `sudo lsof -i :5000` to find running processes on port
# `kill -9 <pid>`



