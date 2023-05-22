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
from models import User,Picture_FER_Usage_Record,Video_FER_Usage_Record,Camera_FER_Usage_Record
from datetime import date,datetime
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
            return {'msg':'账号或密码为空','flag':'0'}
        user=User.query.filter(User.number==number).first()
        if not user:
            return {'msg':'该用户不存在','flag':'0'}
        else :
             if check_password_hash(user.password, password):
                return {'msg':'登录成功','flag':'1'}
             else :
                return {'msg':'密码不正确','flag':'0'}
api.add_resource(Login,'/login/')

class Register(Resource):
    def post(self):
        number=request.json['number']
        password=request.json['password']
        #name=request.json['username']
        hash_password=generate_password_hash(password, method='sha256')
        user=User.query.filter(User.number==number).first()
        if not user :
            try:
                new_user=User(number=number,password=hash_password)
                db.session.add(new_user)
                db.session.commit()
            except:
                db.session.rollback()
            return {'msg':'注册成功','flag':'1'}
        else :
            try:
                user.password=hash_password
                db.session.commit()
            except:
                db.session.rollback()
            return {'msg':'找回密码密码成功','flag':'1'}
        return {'msg':'注册出错','flag':'0'}
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
            return {"msg":"密码修改成功"}
        else:
            return {"msg":"原密码不正确"}

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
        return {'msg':'用户名修改成功'}

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
        return {'msg':"修改头像成功"}
        
class Get_user_profile(Resource):
    def get(self,number):
        user=User.query.filter(User.number==number).first()
        datas=[]
        name=user.name
        avatar=user.avatar
        datas.append({'name':name,'avatar':avatar})
        return {'datas':datas}



class Picture_usage_record_get(Resource):  #获取图片人脸表情识别使用记录
    def get(self,number):
        user=User.query.filter(User.number==number).first()
        picture_records=Picture_FER_Usage_Record.query.filter(Picture_FER_Usage_Record.uid==user.uid).all()
        datas=[]
        for record in picture_records:
            pid=record.pid
            name=user.name
            picture_address=record.picture_address
            result=record.result
            picturetime=json.dumps(record.picturetime,default=str)
            datas.append({'pid':pid,'name':name,'picture_address':picture_address,'result':result,'picturetime':picturetime})
        return {'datas':datas,'lens':len(datas)}

api.add_resource(Picture_usage_record_get,'/get_picture_record/<string:number>')

class Video_usage_record_get(Resource):
    def get(self,number):
        print(number)
        user=User.query.filter(User.number==number).first()
        video_records=Video_FER_Usage_Record.query.filter(Video_FER_Usage_Record.uid==user.uid).all()
        datas=[]
        for record in video_records:
            vid=record.vid
            videotime=json.dumps(record.videotime,default=str)
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
            cameratime=json.dumps(record.cameratime,default=str)
            usagetime=record.usagetime
            datas.append({'cid':cid,'usagetime':usagetime,'cameratime':cameratime})
        return {'datas':datas,'lens':len(datas)}
    
    
class Picture_usage_record_add(Resource): #添加图片表情识别操作记录  
    def post(self):
        number=request.json['number']
        uid=User.query.filter(User.number==number).first().uid
        result=request.json['result']
        picture_address=request.json['picture_address']
        new_usage_record=Picture_FER_Usage_Record(uid=uid,result=result,picture_address=picture_address)
        try:
            # print("yes")
            #print(new_usage_record)
            db.session.add(new_usage_record)
            db.session.commit()
        except:
            print("no")
            db.session.rollback()
        return {'msg':"Added successfully"}
api.add_resource(Picture_usage_record_add,'/add_picture_record/')

    #基于上传视频的人脸表情识别 记录添加 ok
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
    #基于摄像头的表情识别，记录添加  
class Camera_usage_record_add(Resource):
    def post(self):
        number=request.json['number']
        uid=User.query.filter(User.number==number).first().uid
        usagetime=request.json['usagetime']
        new_usage_record=Camera_FER_Usage_Record(uid=uid,usagetime=usagetime)
        try:
            db.session.add(new_usage_record)
            print("yes")
            db.session.commit()
        except:
            print('No')
            db.session.rollback()
        return {'msg':"Added successfully"}

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
                #print(data)
                current_user = User.query.filter(User.number==data['number']).first()
                print(current_user)
            except:
                return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated



api.add_resource(Get_user_profile,'/get_user_profile/<string:number>')

api.add_resource(Video_usage_record_get,'/get_video_record/<string:number>')
api.add_resource(Camera_usage_record_get,'/get_camera_record/<string:number>')

api.add_resource(Video_usage_record_add,'/add_video_record/')
api.add_resource(Camera_usage_record_add,'/add_camera_record/')
api.add_resource(Modify_avatar,'/modify_avatar/')

api.add_resource(Modify_name,'/modify_name/')
api.add_resource(Register,'/register/')
api.add_resource(Modify_password,'/modify_password/')
if __name__ == '__main__':        #运行flask
    app.run(host="localhost",port=5000,debug=True)
