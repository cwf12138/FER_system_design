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
import jwt
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

class Login(Resource):
    def post(self):
        number=request.json['number']
        password=request.json['password']
        if not number or not password:
            return {'msg':'number or password is missing'}
        user=User.query.filter(User.number==number).first()
        if check_password_hash(user.password, password):
            token = jwt.encode({'number' : number, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},key=SALT, algorithm="HS256", headers=headers)
            return jsonify({'token' : token.encode('UTF-8').decode('UTF-8')})

class Register(Resource):
    def post(self):
        number=request.json['number']
        password=request.json['number']
        hash_password=generate_password_hash(password, method='sha256')
        user=User.query.filter(User.number==number).first()
        if not user :
            try:
                new_user=User(number=number,password=hash_password,permisson='0')
                db.session.add(new_user)
                db.session.commit()
            except:
                db.session.rollback()
            return {'msg':'Successfully added a new user'}
        else :
            return {'msg':'This phone number has already been registered, please try again with another phone number'}
        return {"meg":"register is false"}
class Modify_password(Resource):
    def post(self):
        number=request.json["number"]
        oldpassword=request.json["oldpassword"]
        newpassword=request.json["newpassword"]
        user=User.query.filter(User.number==number).first()
        if check_password_hash(user.password, oldpassword):
            try:
                hash_password=generate_password_hash(newpassword, method='sha256')
                user.password=hash_password
                db.session.commit()
            except:
                db.session.rollback()
            return {"msg":"password has been updated"}
        else:
            return {"msg":"Incorrect initial password"}

class Modify_name(Resource):
    def post(self):
        number=request.json['number']
        name=request.json['name']
        user=User.query.filter(User.number==number).first()
        try:
            user.name=name
            db.session.commit()
        except:
            db.session.rollback()
        return {'msg':'Successfully modified username'}

class Modify_avatar(Resource):
    def post(self):
        avatar=request.json['avatar']
        number=request.json['number']
        user=User.query.filter(User.number==number).first()
        try:
            user.avatar=avatar
            db.session.commit()
        except:
            db.session.rollback()
        return {'msg':"Successfully modified the profile picture"}
        

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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({"msg":"token is missing"})
        if auth and auth.startswith('Bearer '):
            token=auth[7:]
            print(token)
            try:
                data = jwt.decode(token,SALT, algorithms=['HS256'])
                print(data)
                current_patient = Patient.query.filter(Patient.account==data['account']).first()
                print(current_patient)
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_patient, *args, **kwargs)

    return decorated




api.add_resource(Picture_usage_record_get,'/get_picture_record/<string:number>')
api.add_resource(Video_usage_record_get,'/get_video_record/<string:number>')
api.add_resource(Camera_usage_record_get,'/get_camera_record/<string:number>')
api.add_resource(Picture_usage_record_add,'/add_picture_record/')
api.add_resource(Video_usage_record_add,'/add_video_record/')
api.add_resource(Camera_usage_record_add,'/add_camera_record/')
api.add_resource(Modify_avatar,'/modify_avatar/')
api.add_resource(Login,'/login/')
api.add_resource(Modify_name/'modify_name/')
api.add_resource(Register,'/register/')
api.add_resource(Modify_password/'modifypassword/')
if __name__ == '__main__':        #运行flask
    app.run(host="localhost",port=5000,debug=True)
