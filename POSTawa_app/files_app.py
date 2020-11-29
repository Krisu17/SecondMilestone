from flask import Flask, render_template, send_file, request, jsonify, redirect, url_for, abort, make_response
import logging
from const import *
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_claims)
import redis
import os
import json
from flask_cors import CORS, cross_origin
import uuid
from model.waybill import *

app = Flask(__name__, static_url_path="")
db = redis.Redis(host="redis", port=6379, decode_responses=True)
log = app.logger
cors = CORS(app)

FILES_PATH = "waybill_files/"
PATH_AND_FILENAME = "path_and_filename"
IMAGES_PATH = "waybill_files/images"
FILENAMES = "filenames"

app.config["JWT_SECRET_KEY"] = os.environ.get(SECRET_KEY)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES_IN_SECONDS
ACCEPTED_IMAGE_EXTENSIONS = ["png", "jpeg", "jpg"]

jwt = JWTManager(app)



@app.before_first_request
def setup():
    log.setLevel(logging.DEBUG)


@app.route("/")
def index():
    return render_template("index-files.html")



@cross_origin(origins=["https://localhost:8080/"], supports_credentials=True)
@app.route("/waybill/<string:waybill_hash>", methods=[GET])
@jwt_required
def download_waybill(waybill_hash):
    user = get_jwt_identity();
    jwt_claims = get_jwt_claims()
    if waybill_hash not in jwt_claims:
        abort(401)
    filename = waybill_hash + ".pdf"
    file_path = os.path.join(FILES_PATH, filename)
    if(not os.path.isfile(file_path)):
        waybill = waybill_form_db(waybill_hash)
        waybill.create_file(FILES_PATH)
    return send_file(file_path)


@app.errorhandler(400)
def bad_request(error):
    response = make_response(render_template("errors/400.html", error=error))
    return response

@app.errorhandler(401)
def unauthorized(error):
    response = make_response(render_template("errors/401.html", error=error))
    return response

@app.errorhandler(403)
def forbidden(error):
    response = make_response(render_template("errors/403.html", error=error))
    return response

@app.errorhandler(404)
def page_not_found(error):
    response = make_response(render_template("errors/404.html", error=error))
    return response

@app.errorhandler(500)
def internal_server_error(error):
    response = make_response(render_template("errors/500.html", error=error))
    return response


