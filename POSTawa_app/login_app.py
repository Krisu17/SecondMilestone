from flask import Flask, render_template, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from const import *
import redis
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path="")
db = redis.Redis(host="redis-db", port=6379, decode_responses=True)

app.config["JWT_SECRET_KEY"] = os.environ.get(SECRET_KEY)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES_IN_SECONDS

jwt = JWTManager(app)
cors = CORS(app)


@cross_origin(origins=["https://localhost:8081/"], supports_credentials=True)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@cross_origin(origins=["https://localhost:8081/"], supports_credentials=True)
@app.route("/register", methods=[GET])
def register():
    return render_template("register.html")

@cross_origin(origins=["https://localhost:8081/"], supports_credentials=True)
@app.route("/login", methods=[GET])
def login():
    return render_template("login.html")





@app.route("/secret", methods=[GET])
@jwt_required
def secret():
    return {"secret_info": "herbata czarna myśli rozjaśnia"}

