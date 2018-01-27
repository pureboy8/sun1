#-*- coding:utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash, request,g
from functools import wraps
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from sqlalchemy import and_,or_
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField,PasswordField
# from wtforms.validators import DataRequired
import time
# import hashlib
# from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from models import User,Role
import config
import sys
reload(sys)
sys.setdefaultencoding('utf8')


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


# @app.context_processor
# def my_context_processor():
#     user_id=session.get('user_id')
#     if user_id:
#         user=User.query.filter(User.id == user_id).first()
#         if user:
#             return {'user': user}
#         return {}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.template_filter('resve')
def reverse_filter(s):
    return  "%s/%s/%s" %(s.year,s.month,s.day)

# def format_datetime(value, format='medium'):
#     if format == 'full':
#         format="EEEE, d. MMMM y 'at' HH:mm"
#     elif format == 'medium':
#         format="y.MM.dd"
#     return babel.dates.format_datetime(value, format)
#app.jinja_env.filters['datetime'] = format_datetime

@app.template_filter('datetime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format="%Y-%m-%d"
    return native.datetime(format) 

#def reverse_filter(s):
#    return s[::-1]
#app.jinja_env.filters['reverse'] = reverse_filter

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_id=session.get('user_id')
    user = User.query.filter_by(id=user_id).first()  # form.name.data
    approve_count=Role.query.join(User,Role.userid==User.mailaddress).filter(or_(User.approve1==user.username,User.approve2==user.username,User.approve3==user.username)).filter(Role.approve_flag.in_([0,2])).count()
    role=Role.query.filter(Role.userid==user.mailaddress).filter(Role.approve_flag.in_([0,1,2])).all()
    approve_data=""
    if approve_count>0:
        approve_data=Role.query.join(User,Role.userid==User.mailaddress).filter(or_(User.approve1==user.username,User.approve2==user.username,User.approve3==user.username)).filter(Role.approve_flag.in_([0,2])).all()
        return render_template('index.html',user=user,log_user=user.username,role=role,approve_count=approve_count,approve=approve,approve_data=approve_data)
    return render_template('index.html',user=user,log_user=user.username,role=role,approve_count=approve_count,approve=approve,approve_data=approve_data)


@app.route('/approve/',methods=['GET', 'POST'])
@login_required
def approve():
    #q=request.args.get('q')
    if request.method == 'POST':
        #user_id = session.get('user_id')
        #user = User.query.filter_by(id=user_id).first()  # form.name.data
        roleid= request.form.get('id1')
        role=Role.query.filter(Role.id==roleid).first()
        mailaddress=role.userid
        user = User.query.filter(User.mailaddress==mailaddress).first()
        if request.values.get('req_text') =="0":#同意审批
            role.approve_flag=role.approve_flag+1
            if role.approve_flag==3:
                user.add_day=user.add_day+role.request_time
        else:#不同意审批
            role.approve_flag= -1 
            role.reason=role.reason+"["+user.username+"]:"+request.values.get('req_text')
            if role.request_flag== 1:
                user.add_day=user.add_day+ role.request_time
            if role.request_flag== 2:
                user.val_date=user.val_date+ role.request_time
            if role.request_flag== 3:
                user.holiday=user.holiday+ role.request_time 
        db.session.add(role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))           
        #return render_template('index.html', user=user)


@app.route('/req2/', methods=['GET', 'POST'])
@login_required
def request2():
    if request.method == 'POST':
        apptime= request.values.get('apptime')
        roleid= request.values.get('id')
        reason= request.values.get('reason')
        role=Role.query.filter(Role.id==roleid).first()
        role.approve_flag=role.approve_flag+1 #2    
        role.request_time=apptime
        role.reason=reason
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('index')) 
    else:
        user_id=session.get('user_id')
        user = User.query.filter_by(id=user_id).first()  # form.name.data
        role=Role.query.filter(Role.userid==user.mailaddress).filter(Role.approve_flag.in_([1])).all()
        return render_template('request2.html',role=role)


@app.route('/req/', methods=['GET', 'POST'])
@login_required
def req():
    if request.method == 'GET':
        return render_template('request.html')
    else:
        request_type = request.form.get('request_type')
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        request_date= datetime.strptime(request.form.get('request_date'),'%Y-%m-%d')
        request_type= int(request.form.get('request_type'))
        requst_time = int(request.form.get('request_time'))
        request_reason= request.form.get('request_reason')
        if request_type== 1:
            if requst_time>user.add_day:
                flash(u'已经超过你的可调休时间，你不可申请！')
                return render_template('request.html')
            else:
                user.add_day=user.add_day-requst_time
        if request_type== 2:
            if requst_time>user.val_date:
                flash(u'你己经没有有薪假了，你不可申请！')
                return render_template('request.html')
            else:
                user.val_date=user.val_date-requst_time
        if request_type== 3:
            if requst_time>user.holiday:
                flash(u'你己经没有追加假期，你不可申请！')
                return render_template('request.html')
            else:
                user.holiday=user.holiday-requst_time
                print user.holiday        
        #print request_type
        #user_id = session.get('user_id')
        #user = User.query.filter_by(id=user_id).first()
        role=Role(userid=user.mailaddress,    name=user.username,
                  request_date=request_date,   request_time=requst_time,
                  request_flag=request_type,
                  reason=request_reason,       approve_flag=0)
        db.session.add(role)
        db.session.add(user)
        db.session.commit()
        flash(u'申请已提交')
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()  # form.name.data
        return redirect(url_for('index'))
        #return render_template('index.html', user=user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        log_user="test"
        return render_template('login.html',log_user=log_user)
    else:
        user = User.query.filter_by(mailaddress=request.form.get('mailaddress')).first()#form.name.data
        password=request.form.get('password')
        if user is None:
            flash( u'用户不存在')
            return render_template('login.html')
        else:
            if user.password_hash!=password:
                flash( u'密码不对')
                return render_template('login.html')
            else:
                session['user_id'] = user.id
                g.log_user=user.id
                #return render_template('index.html', log_user="aaa")
                return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    if session.get('user_id'):
        session.pop('user_id')
        flash( u'用户已经登出')
    return render_template('login.html')


@app.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('passwd.html')
    else:
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password!=password2:
            flash( u'两次密码不同')
            return redirect(url_for('change_password'))
        user_id=session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        user.password_hash=password
        db.session.add(user)
        db.session.commit()
        flash("密码已经变更")
        return redirect(url_for('index'))


@app.route('/alllist/')
def alllist():
    page=request.args.get('page',1,type=int)
    pagination=Role.query.filter(Role.request_flag!=-1).order_by(Role.request_date.desc()).paginate(page,per_page=5,error_out=False)
    role=pagination.items
    return render_template('alllist.html',pagination=pagination,role=role)



@app.route('/mylist/')
@login_required
def mylist():
    user_id=session.get('user_id')
    user = User.query.filter_by(id=user_id).first()  # form.name.data
    page=request.args.get('page',1,type=int)
    pagination=Role.query.filter(Role.userid==user.mailaddress).order_by(Role.create_time.desc()).paginate(page,per_page=5,error_out=False)
    role=pagination.items
    return render_template('mylist.html',user=user,pagination=pagination,role=role)


@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        mailaddress = request.form.get('mailaddress')
        username = request.form.get('username')
        password = request.form.get('password')
        val_date = request.form.get('val_date')
        holiday = request.form.get('holiday')
        add_day = request.form.get('add_day')
        department = request.form.get('department')
        approve1 = request.form.get('approve1')
        approve2 = request.form.get('approve2')
        approve3 = request.form.get('approve3')
        user=User(mailaddress=mailaddress,username=username,password_hash=password,
                  val_date=val_date,holiday=holiday,add_day=add_day,department=department,
                  approve1=approve1,approve2=approve2,approve3=approve3)
        db.session.add(user)
        db.session.commit()
        flash("用户已经追加")
        return redirect(url_for('userlist'))


@app.route('/userlist/', methods=['GET', 'POST'])
@login_required
def userlist():
    if request.method == 'GET':
        users= User.query.all()
        return render_template('userlist.html',users=users)
    else:
        if request.form.get('username'):
            mailaddress = request.form.get('mailaddress')
            username = request.form.get('username')
            val_date = request.form.get('val_date')
            holiday = request.form.get('holiday')
            add_day = request.form.get('add_day')
            department = request.form.get('department')
            approve1 = request.form.get('approve1')
            approve2 = request.form.get('approve2')
            approve3 = request.form.get('approve3')
            user = User.query.filter_by(mailaddress=mailaddress).first()
            user.username=username
            user.val_date=val_date
            user.holiday=holiday
            user.add_day=add_day
            user.department=department
            user.approve1=approve1
            user.approve2=approve2
            user.approve3=approve3
            db.session.add(user)
            db.session.commit()
        users = User.query.all()
        return render_template('userlist.html', users=users)


if __name__=='__main__':
    app.run(debug=True)