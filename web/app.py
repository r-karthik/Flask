from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentenceDataTables
users = db["Users"]

def verifyPw(userName,Password):
    hashed_pw = users.find({
        "userName":userName
    })[0]['Password']

    if bcrypt.hashpw(Password.encode('utf8'),hashed_pw) == hashed_pw:
        return True
    else:
        return False

def verifyTokens(userName):
    Tokens = users.find({
        "userName":userName
    })[0]["Tokens"]
    return Tokens

def updateTokens(userName,no_of_tokens):
    users.update({
            "userName" : userName
        },{
            "$set":{
                    "Tokens":no_of_tokens-1
                    }
        })



class Register(Resource):
    def post(self):
        postedData = request.get_json()
        #get data
        userName = postedData["userName"]
        Password = postedData["Password"]

        hashed_pw = bcrypt.hashpw(Password.encode('utf8'), bcrypt.gensalt())

        #store username & pass in DB
        users.insert({
            "userName" : userName,
            "Password" : hashed_pw,
            "Sentence" : "",
            "Tokens" : 6
        })

        retJson = {
            "status": 200,
            "message" : "You successfully signed up fot the API"
        }

        return jsonify(retJson)

class Store(Resource):
    def post(self):
        postedData = request.get_json()
        #get data
        userName = postedData["userName"]
        Password = postedData["Password"]
        Sentence = postedData["Sentence"]
        #verify userName & Password
        correct_pw = verifyPw(userName,Password)

        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)
        #verify is he having enough tokens

        no_of_tokens = verifyTokens(userName)
        if no_of_tokens <= 0:
            retJson = {
                "status" : 301
            }
            return jsonify(retJson)
        #store the sentence, take a token away & return 200 ok
        users.update({
            "userName" : userName
        },{
            "$set":{
                    "Sentence":Sentence,
                    "Tokens":no_of_tokens-1
                    }
        })

        retJson = {
            "ststus":200,
            "message":"sentence saved successfully"
        }

        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()
        #get data
        userName = postedData["userName"]
        Password = postedData["Password"]
        #verify userName & Password
        correct_pw = verifyPw(userName,Password)
        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)
        #verify is he having enough tokens

        no_of_tokens = verifyTokens(userName)
        if no_of_tokens <= 0:
            retJson = {
                "status" : 301
            }
            return jsonify(retJson)
        
        Sentence = users.find({
            "userName":userName
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "Sentence" : Sentence
        }

        updateTokens(userName,no_of_tokens)

        return jsonify(retJson)




api.add_resource(Register,'/register')
api.add_resource(Store,'/store')
api.add_resource(Get,'/get')

if __name__ == "__main__":
    app.run(host='0.0.0.0')


"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    "num_of_users":0
})

class Visit(Resource):
    def get(self):
        prev_users = UserNum.find({})[0]["num_of_users"]
        new_num = prev_users + 1
        UserNum.update({},{"$set":{"num_of_users": new_num}})
        return str("Hello user " + str(new_num))



def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Add the posted data
        ret = x+y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        #If I am here, then the resouce Subtract was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Subtract the posted data
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
        #If I am here, then the resouce Multiply was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If I am here, then the resouce Divide was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)



api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit,"/hello")

@app.route('/')
def hello_world():
    return "Hello World!"


if __name__=="__main__":
    app.run(host='0.0.0.0')

"""
