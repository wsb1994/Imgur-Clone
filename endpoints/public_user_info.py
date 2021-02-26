# this calms the damn linter which doesn't understand the import

from flask import Blueprint, render_template, request, make_response, jsonify, send_file, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from bson.json_util import dumps, loads
import json
import uuid
import re
import jwt
import time
import pymongo
from pymongo import MongoClient

from .image import image as image_helper

from . import config
user_info = Blueprint('user_info', __name__)

connection_string = config.connection_string
secret_key = config.secret_key


# sanity check route
@user_info.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('user pong!')


@user_info.route('/upload_image', methods=['POST'])
def upload_image():
    encoded = request.headers.get('jwt')
    image = request.headers.get('image')
    tagline = request.headers.get('tagline')
    client = pymongo.MongoClient(connection_string)
    mydb = client['clonegur']
    application_users = mydb['users']
   
    try:
        token = jwt.decode(encoded, secret_key, algorithms="HS256")
        user = dumps(application_users.find({"username": token['username']}))
        user = loads(user)
        user = user[0]
    except Exception as e:
        print(e)
        return make_response('Verification Failure', 401, {'WWW-Authenticate': 'Basic realm="login Required"'})
    images = user['images']
    images.append(image_helper.image(image, tagline).toJSON())

    filter = {'username': token['username']}
    updated = {'$set': {'images': images}}

    application_users.update_one(filter, updated)

    return {'success': 1}


@user_info.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    encoded = request.headers.get('jwt')
    image = request.headers.get('image')
    image = image_helper.image(image, 'avatar').toJSON()

    client = pymongo.MongoClient(connection_string)
    mydb = client['clonegur']
    application_users = mydb['users']

    try:
        token = jwt.decode(encoded, secret_key, algorithms="HS256")
    except Exception as e:
        print(e)
        return make_response('Verification Failure', 401, {'WWW-Authenticate': 'Basic realm="login Required"'})

    filter = {'username': token['username']}
    updated = {'$set': {'avatar': image}}

    application_users.update_one(filter, updated)

    return {'success': 1}

@user_info.route('/user_info/<user>', methods=['GET'])
def pub_info(user):
    client = pymongo.MongoClient(connection_string)
    mydb = client['clonegur']
    application_users = mydb['users']

    try:
        user = dumps(application_users.find({"username": user}))
        user_info = loads(user)
        user_info = user_info[0]
        user_info.pop("password")
        user_info.pop("_id")
    except Exception as e:
        user = {'error': e}
    # TODO verify user info exists

    

    return jsonify(user_info)

