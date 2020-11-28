from flask import Flask, render_template, send_file, request
import logging
from const import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import redis
import os
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path="")
db = redis.Redis(host="redis", port=6379, decode_responses=True)
log = app.logger
cors = CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ.get(SECRET_KEY)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES_IN_SECONDS

jwt = JWTManager(app)



@app.before_first_request
def setup():
    log.setLevel(logging.DEBUG)


@app.route("/")
def index():
    return render_template("index-files.html")


@cross_origin(origins=["https://localhost:8080/"], supports_credentials=True)
@app.route("/register/<string:new_user>")
def is_login_taken(new_user):
    empty = {}
    dbResponse = db.hgetall(new_user)
    if dbResponse == empty:
        return {"message": "User don't exist"}, 404
    else:
        return {"message": "Username already taken"}, 200


@cross_origin(origins=["https://localhost:8080/"], supports_credentials=True)
@app.route("/register/create_new_user/<string:new_user>", methods=[POST])
def create_new_user(new_user):
    name = request.form['name']
    surname = request.form['surname']
    birthDate = request.form['birthDate']
    street = request.form['street']
    adressNumber = request.form['adressNumber']
    postalCode = request.form['postalCode']
    country = request.form['country']
    login = request.form['login']
    pesel = request.form['pesel']
    password = request.form['password']
    if(
        db.hset(login, "name", name) != 1 or
        db.hset(login, "surname", surname) != 1 or
        db.hset(login, "birthDate", birthDate) != 1 or
        db.hset(login, "street", street) != 1 or
        db.hset(login, "adressNumber", adressNumber) != 1 or
        db.hset(login, "postalCode", postalCode) != 1 or
        db.hset(login, "country", country) != 1 or
        db.hset(login, "pesel", pesel) != 1 or
        db.hset(login, "password", password) != 1 
    ):
        db.hdel(login, "name", "surname", "birthDate", "street", "adressNumber", "postalCode", "country", "pesel", "password")
        return {"message": "Something went wrong while adding new user"}, 400
    else:
        return {"message": "User created succesfully"}, 201


@cross_origin(origins=["https://localhost:8080/"], supports_credentials=True)
@app.route("/<string:user>", methods=[GET])
def return_user(user):
    return db.hgetall(user)


@cross_origin(origins=["https://localhost:8080/"], supports_credentials=True)
@app.route("/login_user", methods=[POST])
def log_user():
    login = request.form['login']
    password = request.form['password']
    if (db.hget(login, "password") == password):
        access_token = create_access_token(identity=login)
        db.hset(login, "access_token", access_token)
        # db.expire(login, "access_token", TOKEN_EXPIRES_IN_SECONDS)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Login or password incorrect."}, 400


@app.route("/login/generate_token", methods=[POST])
def generate_token():
    username = request.form["username"]
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}


@app.route("/download-files/", methods=[GET])
@jwt_required
def download_file():
    try:
        full_filename = os.path.join(FILES_PATH, "sdm.pdf")
        return send_file(full_filename)
    except Exception as e:
        log.error("File not found :(")
        log.error(str(e))
        return {"message": "File not found... :("}, 404


@app.route("/upload-file", methods=[POST])
def upload_file():
    maybe_file = request.files["shipment_img"]
    save_file(maybe_file)
    return {"message": "Maybe saved the file."}


def save_file(file_to_save):
    if len(file_to_save.filename) > 0:
        path_to_file = os.path.join(FILES_PATH, file_to_save.filename)
        file_to_save.save(path_to_file)
    else:
        log.warn("Empty content of file!")
