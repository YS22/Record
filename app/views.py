# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid,models,admin
from flask.ext.admin.contrib.sqla import ModelView
from flask_admin import BaseView,expose
from models import User, Modules
from forms import LoginForm, AdminForm,QueryForm
import datetime
import time 
import json
from sqlalchemy import and_,or_
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#web
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Modules, db.session))

# class Query(BaseView):
#     @expose('/', methods=['GET'])
#     def index(self):
#         # form = QueryForm()
#         return redirect(url_for('query'))

class Logout(BaseView):
    @expose('/', methods=['GET'])
    def index(self):
        return redirect(url_for('logout'))

# admin.add_view(Query(name=u'返回查询页'))
admin.add_view(Logout(name=u'退出登陆'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['POST','GET'])
@oid.loginhandler
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password==form.password.data:
            login_user(user, form.remember_me.data)
            if user.username=="admin":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('query'))  
        flash(u'密码或用户名错误!')
    return render_template('login.html', form=form)


@app.route('/admin', methods=['POST','GET'])
@login_required
def admin():
    return ""


@app.route('/query', methods=['POST','GET'])
@login_required
def query():
    form=QueryForm()
    if form.number.data:
        Number = form.number.data
        if form.testTool.data:
            if form.starttime.data and form.stoptime.data:
                modules3 = Modules.query.filter(Modules.number.like('%'+str(Number)+'%')).all()
                modules1=Modules.query.filter_by(testTool = form.testTool.data).all()
                modules2=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                all_modules = list(set(modules1).intersection(set(modules2)))
                modules = list(set(modules3).intersection(set(all_modules)))
                return render_template('query.html',form=form,modules=modules)
                #modules1=Modules.query.filter_by(number = Number,testTool = form.testTool.data).all()
                #modules2=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                #modules=list(set(modules1).intersection(set(modules2)))
                #return render_template('query.html',form=form,modules=modules)
            else:
                #modules=Modules.query.filter_by(number=form.number.data,testTool = form.testTool.data).all()
                #return render_template('query.html',form=form,modules=modules)
                modules1=Modules.query.filter(Modules.number.like('%'+str(Number)+'%')).all()
                modules2=Modules.query.filter_by(testTool = form.testTool.data).all()
                modules=list(set(modules1).intersection(set(modules2)))
                return render_template('query.html',form=form,modules=modules)


        else:
            if form.starttime.data and form.stoptime.data:
                modules1=Modules.query.filter(Modules.number.like('%'+str(Number)+'%')).all()
                modules2=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                modules=list(set(modules1).intersection(set(modules2)))
                return render_template('query.html',form=form,modules=modules)
            else:
                #print number
                #共单号查询
                #modules=Modules.query.filter_by(number=form.number.data).all()
                #return render_template('query.html',form=form,modules=modules)
                modules=Modules.query.filter(Modules.number.like('%'+str(Number)+'%')).all()
                return render_template('query.html',form=form,modules=modules)


    else:
        if form.testTool.data:
            if form.starttime.data and form.stoptime.data:
                modules1=Modules.query.filter_by(testTool = form.testTool.data).all()
                modules2=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                modules=list(set(modules1).intersection(set(modules2)))
                return render_template('query.html',form=form,modules=modules)
            else:
                modules=Modules.query.filter_by(testTool = form.testTool.data).all()
                return render_template('query.html',form=form,modules=modules) 
        else:
            if form.starttime.data and form.stoptime.data:
                modules=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                return render_template('query.html',form=form,modules=modules)
            else:
                modules=""
                return render_template('query.html',form=form,modules=modules)
    modules=""
    return render_template('query.html',form=form,modules=modules)




#api
@app.route('/v1.0/login', methods=['POST'])
def apilogin():
    username=request.json['username']
    password=request.json['password']
    user=User.query.filter_by(username=username).first()
    if user:
        if password==user.password:
            return json.dumps("loginOK")
    else:
        return json.dumps("没有该用户")


@app.route('/v1.0/upload', methods=['POST'])
def upload():

    '''接收数据，根据类型和工单号查看有无存在相同的工单号和类型,有则覆盖，无就加入数据库'''
    type = request.json['type']
    number =request.json['number']
    maxPress =request.json['maxPress']
    minPress = request.json['minPress']
    press = request.json['press']
    maxPressPosition = request.json['maxPressPosition']
    minPressPosition = request.json['minPressPosition']
    pressPosition = request.json['pressPosition']
    minPressPower = request.json['minPressPower']
    maxPressPower = request.json['maxPressPower']
    pressPower = request.json['pressPower']
    maxPressStroke = request.json['maxPressStroke']
    minPressStroke = request.json['minPressStroke']
    pressStroke = request.json['pressStroke']
    maxBack = request.json['maxBack']
    minBcak = request.json['minBcak']
    back = request.json['back']
    maxBackPosition = request.json['maxBackPosition']
    minBackPosition = request.json['minBackPosition']
    backPosition = request.json['backPosition']
    minBackPower = request.json['minBackPower']
    maxBackPower = request.json['maxBackPower']
    backPower = request.json['backPower']
    maxBackStroke = request.json['maxBackStroke']
    minBackStroke = request.json['minBackStroke']
    backStroke = request.json['backStroke']
    testTime = request.json['testTime']
    testTool = request.json['testTool']

    modules=Modules.query.filter_by(type=type,number=number).first()
    if modules:

        modules.type = type
        modules.number = number 
        modules.maxPress = maxPress
        modules.minPress = minPress 
        modules.press = press
        modules.maxPressPosition = maxPressPosition 
        modules.minPressPosition = minPressPosition 
        modules.pressPosition = pressPosition 
        modules.minPressPower = minPressPower 
        modules.maxPressPower = maxPressPower
        modules.pressPower = pressPower 
        modules.maxPressStroke = maxPressStroke
        modules.minPressStroke = minPressStroke
        modules.pressStroke = pressStroke
        modules.maxBack = maxBack 
        modules.minBcak = minBcak 
        modules.back = back
        modules.maxBackPosition = maxBackPosition 
        modules.minBackPosition = minBackPosition 
        modules.backPosition = backPosition 
        modules.minBackPower = minBackPower 
        modules.maxBackPower = maxBackPower
        modules.backPower = backPower 
        modules.maxBackStroke = maxBackStroke
        modules.minBackStroke = minBackStroke
        modules.backStroke = backStroke
        modules.testTime = testTime 
        modules.testTool = testTool

        db.session.add(modules)
        db.session.commit()
        return json.dumps("updata OK")
    
    else:
        modules=Modules(
        type = type,
        number = number ,
        maxPress = maxPress,
        minPress = minPress ,
        press = press,
        maxPressPosition = maxPressPosition,
        minPressPosition = minPressPosition ,
        pressPosition = pressPosition, 
        minPressPower = minPressPower ,
        maxPressPower = maxPressPower,
        pressPower = pressPower,
        maxPressStroke = maxPressStroke,
        minPressStroke = minPressStroke,
        pressStroke = pressStroke,
        maxBack = maxBack ,
        minBcak = minBcak ,
        back = back,
        maxBackPosition = maxBackPosition ,
        minBackPosition = minBackPosition ,
        backPosition = backPosition ,
        minBackPower = minBackPower ,
        maxBackPower = maxBackPower,
        backPower = backPower ,
        maxBackStroke = maxBackStroke,
        minBackStroke = minBackStroke,
        backStroke = backStroke,
        testTime = testTime ,
        testTool = testTool
        )
        db.session.add(modules)
        db.session.commit()
        return json.dumps("upload OK")

@app.route('/v1.0/number', methods=['POST'])
def number():

    ''' 根据工单号查询数据'''
    number=request.json['number']
    modules=Modules.query.filter_by(number=number).all()[0:1]
    modulesInfo=[]
    for module in modules:
        Info={
        'id':module.id,
        'type':module.type,
        'number':module.number ,
        'maxPress':module.maxPress,
        'minPress':module.minPress ,
        'press':module.press,
        'maxPressPosition':module.maxPressPosition,
        'minPressPosition':module.minPressPosition ,
        'pressPosition':module.pressPosition, 
        'minPressPower':module.minPressPower ,
        'maxPressPower':module.maxPressPower,
        'pressPower':module.pressPower,
        'maxPressStroke':module.maxPressStroke,
        'minPressStroke':module.minPressStroke,
        'pressStroke': module.pressStroke,
        'maxBack' : module.maxBack ,
        'minBcak': module.minBcak ,
        'back': module.back,
        'maxBackPosition': module.maxBackPosition ,
        'minBackPosition' : module.minBackPosition ,
        'backPosition': module.backPosition ,
        'minBackPower' : module.minBackPower ,
        'maxBackPower' : module.maxBackPower,
        'backPower' : module.backPower ,
        'maxBackStroke' : module.maxBackStroke,
        'minBackStroke': module.minBackStroke,
        'backStroke' : module.backStroke,
        'testTime':str(module.testTime),
        'testTool' : module.testTool
        }
        modulesInfo.append(Info)
    return json.dumps(modulesInfo)


@app.route('/v1.0/numbertype', methods=['POST'])
def numbertype():
    number=request.json['number']
    type=request.json['type']
    module=Modules.query.filter_by(number=number,type=type).first()
    if module:
        modulesInfo={
            'press':module.press,
            'pressPosition':module.pressPosition, 
            'pressPower':module.pressPower,
            'pressStroke': module.pressStroke,
            'back': module.back,
            'backPosition': module.backPosition ,
            'backPower' : module.backPower ,
            'backStroke' : module.backStroke,
            'testTime':str(module.testTime),
            'testTool' : module.testTool
        }
        return json.dumps(modulesInfo)
    else:
        return json.dumps('')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




 









