from exts import db
from datetime import datetime

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    userid=db.Column(db.String(20),db.ForeignKey('user.mailaddress'))
    name=db.Column(db.String(64))
    request_date=db.Column(db.DateTime,nullable=False)
    request_time=db.Column(db.Integer,nullable=False)
    reason=db.Column(db.Text)
    request_flag=db.Column(db.Integer,default=0)
    approve_flag=db.Column(db.Integer,default=0)
    create_time=db.Column(db.DateTime,default=datetime.now)
    user = db.relationship('User', backref=db.backref('user'))

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablemame__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(20),nullable=False)
    mailaddress=db.Column(db.String(20),unique=True,nullable=False)
    password_hash=db.Column(db.String(128))
    val_date=db.Column(db.Integer,default=0)
    holiday=db.Column(db.Integer,default=0)
    add_day=db.Column(db.Integer,default=0)
    department=db.Column(db.String(10),nullable=False)
    approve1=db.Column(db.String(20))
    approve2=db.Column(db.String(20))
    approve3=db.Column(db.String(20))
    #role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' %self.username

    # @property
    # def password(self):
    #     raise AttributeError('Password Can not be read')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return self.password_hash==password
    #     #return check_password_hash(self.password_hash, password)