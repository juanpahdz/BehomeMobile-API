import re
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, request, jsonify
from passlib.hash import pbkdf2_sha256
import uuid

application = Flask(__name__)
application.secret_key = "123askldaskfbbaskdkasgjash0120fd17237ajkhafkas"

connection = pymongo.MongoClient("mongodb://admin:3023457476@50.19.173.205:27017")
db = connection["fourseasons"]
apartments = db["apartments"]
users = db["users"]

#REGISTRAR USUARIO

@application.route('/')
def home():
    return jsonify({'Status':'Last Version Working'})

@application.route('/createusers', methods=['POST'])
def CreateUsers():

    fullname = request.json['fullname']
    email = request.json['email']
    country = request.json['country']
    city = request.json['city']
    password = request.json['password']

    if fullname and email and country and city and password:

        user = {
            '_id': uuid.uuid4().hex,
            'fullname': fullname,
            'email': email,
            'country': country,
            'city': city,
            'password': password
            }

        user["password"] = pbkdf2_sha256.encrypt(user['password'])

        if users.find_one({"email": user["email"]}):
            return jsonify({"error": "Ese email ya esta registrado"}), 400

        if users.insert_one(user):
            del user["password"]
            return user
  
        return jsonify({'error':'El registro fallo, por favor intenta mas tarde'})

    return jsonify({'error':'necesitas llenar todos los datos antes de enviar'})

#LOGIN VALIDAR USUARIO
@application.route('/login', methods=['POST'])
def Login():
    user = db.users.find_one({"email": request.json['email'] })

    if user and pbkdf2_sha256.verify(request.json['password'], user['password']):
        del user["password"]
        return jsonify(user)

    return jsonify({ "error": "Contraseña Incorrecta" }), 401

   
#LEER TODA LA DATA DE APARTAMENTOS
@application.route('/readallapartments', methods=['GET'])
def ReadAllapArtments():
    result = dumps(apartments.find()) 

    return result


#ELIMINAR APARTAMENTOS
@application.route('/delete', methods=['POST'])
def delete():
    query = {"_id": ObjectId(request.json['id'])}
    apartments.delete_one(query)
    
    return "Registro Eliminado"

#CREATE APARTMENT
@application.route('/createapartments', methods=['POST'])
def createapartments():

    title = request.json['title']
    pricenight = request.json['pricenight']
    numrooms = request.json['numrooms']
    meters = request.json['meters']
    ubicacion = request.json['ubicacion']
    imagenes = request.json['imagenes']

    if title and pricenight and numrooms and meters and ubicacion and imagenes:

        apartment = {
            '_id': uuid.uuid4().hex,
            'title': title,
            'pricenight': pricenight,
            'numrooms': numrooms,
            'meters': meters,
            'ubicacion': ubicacion,
            'imagenes': imagenes,
            }


        if apartments.insert_one(apartment):
            return apartment
  
        return jsonify({'error':'El registro fallo, por favor intenta mas tarde'})

    return jsonify({'error':'necesitas llenar todos los datos antes de enviar'})


if __name__ == "__main__":
    application.run(debug=True)