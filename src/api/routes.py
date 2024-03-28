"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

#metodos copiado de pagi JWT flask python
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email == None or password == None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    
    user = User.query.filter_by(email=email).one_or_none()

    if user != None:

        if password == user.password:
           access_token = create_access_token(identity=email)
           return jsonify(access_token= access_token)
        else:
            return jsonify({"msj": "Wrong password"}), 401
    
    return jsonify({"msj": "User not found"}),404

@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user, is_active = True).one_or_none()
    if user != None:
        return jsonify(user.serialize()), 200
    
    return jsonify({"msj" : "El usuario no esta activo,disculpe contacte a soporte"}), 200
