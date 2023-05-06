from flask_sqlalchemy import SQLAlchemy


#下面就是数据库连接的一些配置，根据自己情况进行修改


db = SQLAlchemy()
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = "root"     #数据库用户名
PASSWORD = "123456" #每个人设置的名字和账号会不同，这里是自己设定的账号密码
HOST = '127.0.0.1'   #ip地址
PORT = '3306'
DATABASE = 'FER_system' #这里是数据库文件名
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
