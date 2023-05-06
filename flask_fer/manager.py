from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from external import db
from models import User,Picture_FER_Usage_Record,Video_FER_Usage_Record,Camera_FER_Usage_Record


migrate = Migrate(app,db)
 
manager = Manager(app)
manager.add_command('db',MigrateCommand)
 
if __name__ == "__main__":
 manager.run()
