#-*- coding:utf-8 -*-
from flask_script import Manager
from hello	import app
from flask_migrate import Migrate,MigrateCommand
from exts import db
from models import User,Role


manager=Manager(app)

migrate =Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
	manager.run()