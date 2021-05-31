import re
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, request

application = Flask(__name__)

connection = pymongo.MongoClient("mongodb://admin:3023457476@50.19.173.205:27017")
db = connection["fourseasons"]
apartments = db["apartments"]
users = db["users"]

#REGISTRAR USUARIO
@application.route('/createusers', methods=['POST'])
def CreateUsers():

    Fullname = request.json['Fullname']
    Email = request.json['Email']
    Country = request.json['Country']
    City = request.json['City']
    Password = request.json['Password']

    if Fullname and Email and Country and City and Password:
        Id = users.insert_one(
            {'Fullname':Fullname, 'Email':Email, 'City':City, 'Password': Password}
        )
        response = {
            'Id': str(Id),
            'Fullname': Fullname,
            'Email': Email,
            'Country': Country,
            'City': City,
            'Password': Password
        }
        return response
    else:
        {'message':'recived'}    
    


    return {'message':'recived'}

#LOGIN VALIDAR USUARIO
@application.route('/login/<string:getemail>/<string:getpassword>', methods=['POST', 'GET'])
def Login(getemail,getpassword):
    query = {"Email": getemail,"Password": getpassword}
    result = users.find(query)
    data = []
    for document in result:
        data.applicationend(document)
    print(data)
    if len(data) >= 1:
        return "1"
    else:
        return "0"

   
#LEER TODA LA DATA DE APARTAMENTOS
@application.route('/readallapartments', methods=['GET'])
def ReadAllapArtments():
    result = dumps(apartments.find()) 

    # data = []
    # for document in result:
    #     data.applicationend(document)

    # l = str(data)
    # data = json.dumps(l)
    # info = json.loads(data)

    return result


#ELIMINAR APARTAMENTOS
@application.route('/delete/<string:getid>', methods=['POST', 'GET'])
def delete(getid):
    query = {"_id": ObjectId(getid)}
    apartments.delete_one(query)
    
    return "Registro Eliminado"


if __name__ == "__main__":
    application.run(debug=True)