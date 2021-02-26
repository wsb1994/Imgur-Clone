# this calms the linter which doesn't understand the import
import time
import jwt
import re
import uuid
import json
from . import image
from . import config
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps, loads
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask import Blueprint, render_template, request, make_response, jsonify, send_file, session

from . import config

from .config import connection_string
from .config import secret_key


auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.form

    username, password = data.get('username'), data.get('password')

    user = {"username": str(username),
            "password": str(generate_password_hash(password)),
            "uuid": str(uuid.uuid4()),
            "user_info": {},
            "images": [],
            "avatar": None,

            }
    # TODO remove password string from source code, use environment variables
    client = pymongo.MongoClient(connection_string)
    mydb = client['clonegur']
    application_users = mydb['users']
    application_users.insert_one(user)

    return {"status": 1}


@auth.route('/login')
def login():
    #auth = request.authorization
    req = request.form
    auth = req.get("username")
    auth_password = req.get("password")
     
    client = pymongo.MongoClient(connection_string)
    mydb = client['clonegur']
    application_users = mydb['users']

    user = dumps(application_users.find({"username": auth}))
    user = loads(user)
    user = user[0]
    if auth == user["username"] and check_password_hash(user["password"], auth_password):
        encoded_jwt = jwt.encode({"username": user["username"], "expiry": float(
            time.time()) + 3600.0}, secret_key, algorithm="HS256")
        return encoded_jwt
    return make_response('Verification Failure', 401, {'WWW-Authenticate': 'Basic realm="login Required"'})


@auth.route('/logout')
def logout():
    return ''


# sanity check route
@auth.route('/auth_ping', methods=['GET'])
def ping_pong():
    return jsonify('auth pong!')
