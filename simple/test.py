#-*- coding:utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash, request
from functools import wraps

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from exts import db
from models import User, Role
import config


app=Flask(__name__)
app.config.from_object(config)

db.init_app(app)#db=SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/req/', methods=['GET','POST'])
@login_required
def req():
    if request.method == 'GET':
        return render_template('request.html')
    else:
        request_date= request.form.get('request_date')
        request_type= request.form.get('request_type')
        request_time= request.form.get('request_time')
        request_reason= request.form.get('request_reason')
        role=Role()
        flash(u'申请已提交')
        return render_template('index.html')

@app.route('/logout/')
def logout():
    if session.get('user_id'):
        session.pop('user_id')
        flash( u'用户已经登出')
    return render_template('login.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = User.query.filter_by(mailaddress=request.form.get('mailaddress')).first()#form.name.data
        password=request.form.get('password')
        if user is None:
            flash( u'用户不存在')
            return render_template('login.html')
        else:
            if user.password_hash<>password:
                flash( u'密码不对')
                return render_template('login.html')
            else:
                session['user_id'] = user.id
                return redirect(url_for('index', user=user))

if __name__ == '__main__':
    app.run(debug=True)