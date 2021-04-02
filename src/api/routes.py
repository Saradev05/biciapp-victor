"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def signup():
    body= request.get_json()
    User.create_user(body["email"], body["password"])
        
    return jsonify({}), 200


@api.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body ["email" ]
    password = body ["pasword"]

    user = User.get_login_credentials(email, password)
    if user is None:
        raise APIException("Email o contraseña incorrecta")

    access_token = create_access_token(identity=user.id )
    return jsonify({"access_token": access_token   })

@api.route('/profile', methods=['GET'])
def profile():
        user= User.get(id)
        return jsonify(user.serialize())
    