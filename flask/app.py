from flask import Flask,request,jsonify,make_response,g
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import external
from werkzeug.security import generate_password_hash, check_password_hash
import requests,json
from flask_cors import CORS
from functools import wraps
from external import db
from models import Admin,User,Picture_FER_Usage_Record,Video_FER_Usage_Record,Camera_FER_Usage_Record
import datetime
app = Flask(__name__)
app.config.from_object(external)
api = Api(app, default_mediatype="application/json")
app.config['SECRET_KEY'] = 'thisissecret'
db.init_app(app)
ma = Marshmallow(app)
CORS(app, resources=r'/*')
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='

@app.route('/')
def index():
 return "Hello!"


class Login(Resource):
    def get(self):
        return 
class Register(Resource):
    def get(self):
        return 
class Modify_password(Resource):
    def get(self):
        return 
class Modify_avatar(Resource):
    def get(self):
        return 

class Picture_usage_record_get(Resource):
    def get(self,number):
        user=User.query.filter(User.number==number).first()
        picture_records=Picture_FER_Usage_Record.query.filter(Picture_FER_Usage_Record.uid==user.uid).all()
        datas=[]
        for record in picture_records:
            pid=record.pid
            name=user.name
            picture_address=record.picture_address
            result=record.result
            picturetime=record.picturetime
            datas.append({'pid':pid,'name':name,'picture_address':picture_address,'result':result,'picturetime':picturetime})
        return {'datas':datas,'lens':len(datas)}

class Video_usage_record_get(Resource):
    def get(self,number):
        user=User.query.filter(User.number==number).first()
        video_records=Video_FER_Usage_Record.query.filter(Video_FER_Usage_Record.uid==user.uid).all()
        datas=[]
        for record in video_records:
            vid=record.vid
            videotime=record.videotime
            usagetime=record.usagetime
            datas.append({'vid':vid,'usagetime':usagetime,'videotime':videotime})
        return {'datas':datas,'lens':len(datas)}
class Camera_usage_record_get(Resource):
    def get(self,number):
        user=User.query.filter(User.number==number).first()
        Camera_records=Camera_FER_Usage_Record.query.filter(Camera_FER_Usage_Record.uid==user.uid).all()
        datas=[]
        for record in Camera_records:
            cid=record.cid
            cameratime=record.cameratime
            usagetime=record.usagetime
            datas.append({'cid':cid,'usagetime':usagetime,'cameratime':cameratime})
        return {'datas':datas,'lens':len(datas)}
class Picture_usage_record_add(Resource):
    def post(self):
        number=request.json['number']
        uid=User.query.filter(User.number==number).first().uid
        result=request.json['result']
        pricture_address=request.json['picture_address']
        new_usage_record=Picture_FER_Usage_Record(uid=uid,result=result,pricture_address=pricture_address)
        try:
            db.session.add(new_usage_record)
            db.session.commit()
        except:
            db.session.rollback()
        return {'msg':"Added successfully"}
class Video_usage_record_add(Resource):
    def post(self):
        number=request.json['number']
        uid=User.query.filter(User.number==number).first().uid
        usagetime=request.json['usagetime']
        new_usage_record=Video_FER_Usage_Record(uid=uid,usagetime=usagetime)
        try:
            db.session.add(new_usage_record)
            db.session.commit()
        except:
            db.session.rollback()
        return {'msg':"Added successfully"}
class Camera_usage_record_add(Resource):
    def post(self):
        number=request.json['number']
        uid=User.query.filter(User.number==number).first().uid
        usagetime=request.json['usagetime']
        new_usage_record=Video_FER_Usage_Record(uid=uid,usagetime=usagetime)
        try:
            db.session.add(new_usage_record)
            db.session.commit()
        except:
            db.session.rollback()


api.add_resource(Picture_usage_record_get,'/get_picture_record/<string:number>')
api.add_resource(Video_usage_record_get,'/get_video_record/<string:number>')
api.add_resource(Camera_usage_record_get,'/get_camera_record/<string:number>')
api.add_resource(Picture_usage_record_add,'/add_picture_record/')
api.add_resource(Video_usage_record_add,'/add_video_record/')
api.add_resource(Camera_usage_record_add,'/add_camera_record/')

if __name__ == '__main__':        #运行flask
    app.run(host="localhost",port=5000,debug=True)
