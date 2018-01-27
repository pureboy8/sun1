import os

#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
#app.config['SECRET_KEY']='you can not guess'
basedir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY='you can not guess'