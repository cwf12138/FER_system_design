from flask import Flask,request,jsonify,make_response,g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import external
from werkzeug.security import generate_password_hash, check_password_hash
import requests,json
from flask_cors import CORS
from external import db
from models import Admin,User,Picture_FER_Usage_Record,Video_FER_Usage_Record,Camera_FER_Usage_Record
import datetime
app = Flask(__name__)
app.config.from_object(external)
api = Api(app, default_mediatype="application/json")
app.config['SECRET_KEY'] = 'thisissecret'
db.init_app(app)
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='

@app.route('/')
def index():
 return "Hello!"
if __name__ == '__main__':        #运行flask
    app.run(host="0.0.0.0",port=5000,debug=True)
