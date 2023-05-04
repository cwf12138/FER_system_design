from external import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    __tablename__="user"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(50))
    number = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(500))
    avater = db.Column(db.String(500))
    permission = db.Column(db.String(50))
    picture_records = db.relationship('Picture_FER_Usage_Record', backref='Puser', cascade='all, delete-orphan', passive_deletes = True)
    video_records = db.relationship('Video_FER_Usage_Record', backref='Vuser', cascade='all, delete-orphan', passive_deletes = True)
    camera_records = db.relationship('Camera_FER_Usage_Record', backref='Cuser', cascade='all, delete-orphan', passive_deletes = True)

class Admin(db.Model):
    __tablename__="admin"
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(50))
    number = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(500))
    avater = db.Column(db.String(500))
    permission = db.Column(db.String(50))

class Picture_FER_Usage_Record(db.Model):
    __tablename__="picture"
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    uid = db.Column(db.Integer, db.ForeignKey('user.uid',ondelete='CASCADE'))
    result = db.Column(db.String(50))
    picturetime =  db.Column(db.DateTime, default=datetime.now)
    picture_address = db.Column(db.String(50))


class Video_FER_Usage_Record(db.Model):
    __tablename__="video"
    vid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid',ondelete='CASCADE'))  
    videotime = db.Column(db.DateTime, default=datetime.now)
    usagetime = db.Column(db.Integer)

class Camera_FER_Usage_Record(db.Model):  
    __tablename__="camera"
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid',ondelete='CASCADE')) 
    cameratime = db.Column(db.DateTime, default=datetime.now)
    usagetime = db.Column(db.Integer)

