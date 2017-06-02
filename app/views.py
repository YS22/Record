# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid,models,admin
from flask.ext.admin.contrib.sqla import ModelView
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['POST','GET'])
@oid.loginhandler
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password==form.password.data:
            login_user(user, form.remember_me.data)
            return redirect(url_for('query'))  
        flash(u'密码或用户名错误!')
    return render_template('login.html', form=form)


@app.route('/admin', methods=['POST','GET'])
@login_required
def admin():
#     form=AdminForm()
#     if form.validate_on_submit():
#         if form.password.data==form.reppassword.data:
#             user=User.query.filter_by(username=form.username.data).first()
#             if user:
#                 flash(u'用户名已被占用')
#                 return redirect(url_for('admin'))
#             else:
#                 user=User(username=form.username.data,password=form.password.data)
#                 db.session.add(user)
#                 db.session.commit()
#                 flash(u'添加成功')
#                 return redirect(url_for('admin'))
#         else:
#             flash(u'二次输入密码不同')
#             return redirect(url_for('admin'))
#     users=User.query.all()[1:]
      return render_template('admin.html',form=form,users=users)


@app.route('/query', methods=['POST','GET'])
@login_required
def query():
    form=QueryForm()
    if form.number.data:
        if form.testTool.data:
            if form.starttime.data and form.stoptime.data:
                modules1=Modules.query.filter_by(number=form.number.data,testTool = form.testTool.data).all()
                modules2=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                modules=list(set(modules1).intersection(set(modules2)))
                return render_template('query.html',form=form,modules=modules)
            else:
                modules=Modules.query.filter_by(number=form.number.data,testTool = form.testTool.data).all()
                return render_template('query.html',form=form,modules=modules)
        else:
            if form.starttime.data and form.stoptime.data:
                modules1=Modules.query.filter_by(number=form.number.data).all()
                modules2=Modules.query.filter(Modules.testTime>=form.starttime.data,Modules.testTime<form.stoptime.data).all()
                modules=list(set(modules1).intersection(set(modules2)))
            else:
                modules=Modules.query.filter_by(number=form.number.data).all()
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
    type=request.json['type']
    number=request.json['number']
    maxPress=request.json['maxPress']
    minPress=request.json['minPress']
    press=request.json['press']
    maxPressPosition=request.json['maxPressPosition']
    minPressPosition=request.json['minPressPosition']
    pressPosition=request.json['pressPosition']
    minPressPower=request.json['minPressPower']
    pressPower=request.json['pressPower']
    maxBack=request.json['maxBack']
    minBcak=request.json['minBcak']
    back=request.json['back']
    maxBackPosition=request.json['maxBackPosition']
    minBackPosition=request.json['minBackPosition']
    backPosition=request.json['backPosition']
    minBackPower=request.json['minBackPower']
    backPower=request.json['backPower']
    testTime=datetime.datetime.now()
    #testTime=request.json['testTime']
    tester=request.json['tester']
    testTool=request.json['testTool']

    modules=Modules.query.filter_by(type=type,number=number).first()
    if modules:
        #modules.maxPress=maxPress
        #modules.minPress=minPress
        modules.press=press
        #modules.maxPressPosition=maxPressPosition
        #modules.minPressPosition=minPressPosition
        modules.pressPosition=pressPosition
        #modules.minPressPower=minPressPower
        modules.pressPower=pressPower
        #modules.maxBack=maxBack
        #modules.minBca=minBca
        modules.back=back
        #modules.maxBackPosition=maxBackPosition
        #modules.minBackPosition=minBackPosition
        modules.backPosition=backPosition
        #modules.minBackPower=minBackPower
        modules.backPower=backPower
        modules.testTime=testTime
        modules.tester=tester
        modules.testTool=testTool
        db.session.add(modules)
        db.session.commit()
        return json.dumps("updata OK")
    
    else:
        modules=Modules(
        type=type,
        number=number,
        maxPress=maxPress,
        minPress=minPress,
        press=press,
        maxPressPosition=maxPressPosition,
        minPressPosition=minPressPosition,
        pressPosition=pressPosition,
        minPressPower=minPressPower,
        pressPower=pressPower,
        maxBack=maxBack,
        minBcak=minBcak,
        back=back,
        maxBackPosition=maxBackPosition,
        minBackPosition=minBackPosition,
        backPosition=backPosition,
        minBackPower=minBackPower,
        backPower=backPower,
        testTime=testTime,
        tester=tester,
        testTool=testTool
        )
        db.session.add(modules)
        db.session.commit()
        return json.dumps("upload OK")

@app.route('/v1.0/number', methods=['POST'])
def number():
    number=request.json['number']
    modules=Modules.query.filter_by(number=number).all()[0:1]
    modulesInfo=[]
    for module in modules:
        Info={
        'id':module.id,
        'type':module.type,
        'number':module.number,
        'maxPress':module.maxPress,
        'minPress':module.minPress,
        'press':module.press,
        'maxPressPosition':module.maxPressPosition,
        'minPressPosition':module.minPressPosition,
        'pressPosition':module.pressPosition,
        'minPressPower':module.minPressPower,
        'pressPower':module.pressPower,
        'maxBack':module.maxBack,
        'minBcak':module.minBcak,
        'back':module.back,
        'maxBackPosition':module.maxBackPosition,
        'minBackPosition':module.minBackPosition,
        'backPosition':module.backPosition,
        'minBackPower':module.minBackPower,
        'backPower':module.backPower,
        'testTime':str(module.testTime),
        'tester':module.tester,
        'testTool':module.testTool
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
        'back':module.back,
        'backPosition':module.backPosition,
        'backPower':module.backPower,
        'testTime':str(module.testTime),
        'testTool':module.testTool
        }
        return json.dumps(modulesInfo)
    else:
        return json.dumps('')







# @app.route('/', methods=['GET', 'POST'])
# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login(): 
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))
#     form = LoginForm() 
#     if form.validate_on_submit():
#         user = User.query.filter_by(nickname=form.nickname.data).first()
#         if user is not None and user.password==form.password.data:
#             login_user(user, form.remember_me.data)
#             return redirect(url_for('index'))  
#         flash(u'密码或用户名错误!')
#     return render_template('login.html', form=form)


# @app.route('/index', methods=['GET', 'POST'])
# @login_required
# def index():
#     role_list=[]
#     ren_lenth=0
#     form = IndexForm()
#     zu = Group.query.filter_by(groupname=form.name.data).first()
#     if form.validate_on_submit():
#         if zu is None :
#             flash(u'此群未建立！')
#         else:
#              ren_list=zu.user.all()
#              ren_lenth=len(ren_list)
#              if g.user in ren_list:
#                 for rens in ren_list:
#                     role_list.append(rens.role[0])   
#              else:
#                 flash(u'你不属于该群成员！')
#                 return redirect(url_for('index'))   
#     group_list= g.user.group.all()
#     position_list=[]
#     name_list=[]
#     tel_list=[]
#     for role in role_list:
#         position_list.append(role.position)
#         name_list.append(role.name)
#         tel_list.append(role.tel)
#     return render_template('index.html',
#                            title='Home',
#                            form=form,
#                            position_list=position_list,name_list=name_list,tel_list=tel_list,role_list=role_list,group_list=group_list,zu=zu,ren_lenth=ren_lenth)

    
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


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(nickname=form.nickname.data,password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash(u'注册成功，请登录！')
#         return redirect(url_for('login'))
#     if User.query.filter_by(nickname=form.nickname.data).first():
#         flash(u'用户名已注册')
#     return render_template('register.html', form=form)
# @app.route('/edit', methods=['GET', 'POST'])
# @login_required
# def edit():
#     form = InfoForm()
#     if form.validate_on_submit():
#         role = Role.query.filter_by(name=form.name.data).first()
#         user_role=g.user.role.all()
#         if user_role==[]:
#             roles= Role(position=form.position.data,name=form.name.data,tel=form.tel.data,author=g.user)
#             db.session.add(roles)
#             db.session.commit()
#             flash(u'信息添加成功！')
#         else:
#             if role is not None:
#                 if  g.user.role[0].name==role.name:
#                     role.position=form.position.data
#                     role.tel=form.tel.data
#                     db.session.add(role)
#                     db.session.commit()
#                     flash(u'信息修改成功！')
                    
#                 else:
#                     flash(u'真实姓名不符，无法修改！') 

#             else:
#                 flash(u'真实姓名不符，无法修改！')

#     role_list= models.Role.query.all()
#     position_list=[]
#     name_list=[]
#     tel_list=[]
#     positions=[]
#     names=[]
#     tels=[]
#     for role in role_list:
#         position_list.append(role.position)
#         name_list.append(role.name)
#         tel_list.append(role.tel)
#     return render_template('edit.html',
#                            title='Home',
#                            form=form,
#                            position_list=position_list,name_list=name_list,tel_list=tel_list,role_list=role_list)


# @app.route('/group', methods=['GET', 'POST'])
# @login_required
# def group():
#     form = EstablishForm()
#     if form.validate_on_submit():
#         l = Group.query.filter_by(groupname=form.name.data).first()
#         user_role=g.user.role.all()
#         if l is None:
#             if user_role==[]:
#                  flash(u'请编辑你的信息再创建群组！')
#                  return redirect(url_for('group'))
#             else:
#                 group = Group(groupname=form.name.data)
#                 db.session.add(group)
#                 db.session.commit()
#                 g.user.group.append(group)
#                 db.session.add(g.user)
#                 db.session.commit()
#                 flash(u'创建成功,你已是该群成员！') 
#         else:
#             flash(u'该名称已被占用！')
#     return render_template('group.html', form=form)

# @app.route('/join', methods=['GET', 'POST'])
# @login_required
# def join():
#     form = JoinForm()
#     if form.validate_on_submit():
#         s = Group.query.filter_by(groupname=form.name.data).first()
#         user_role=g.user.role.all()
#         if s is None:
#             flash(u'此群未建立')
#         else:
#             ren_list=s.user.all()
#             for ren in ren_list:
#                 if ren==g.user:
#                     flash(u'你在该组群，不需重新加入！')
#                     return redirect(url_for('join'))
#             else:
#                 if user_role==[]:
#                     flash(u'请先编辑你的信息，再加入群组！')
#                     return redirect(url_for('join'))
#                 else:
#                     g.user.group.append(s)
#                     db.session.add(g.user)
#                     db.session.commit()
#                     flash(u'加入成功！')                       
#     return render_template('join.html', form=form)

# @app.route('/groupinfo', methods=['GET', 'POST'])
# @login_required
# def groupinfo():
#     group_list=g.user.group.all() 
#     group_lenth=len(group_list)                                                                                                          
#     return render_template('groupinfo.html',group_list=group_list,group_lenth=group_lenth)
    

# @app.route('/dele', methods=['GET', 'POST'])
# @login_required
# def dele():
#       form = JoinForm()
#       role_list=[]
#       zu = Group.query.filter_by(groupname=form.name.data).first()
#       if form.validate_on_submit():
#           if zu is not None:
#                  ren_list=zu.user.all()
#                  if g.user in ren_list:
#                     for rens in ren_list:
#                         role_list.append(rens.role[0])
#                     role_list.remove(g.user.role[0])
#                     g.user.group.remove(zu)
#                     db.session.add(g.user)
#                     db.session.commit()
#                     flash(u'你已从该群移出！')      
#                  else:
#                     flash(u'操作无效，你不是该群成员！')
#                     return redirect(url_for('dele'))
#           else:
#             flash(u'请正确输入群名！')
#             return redirect(url_for('dele')) 
#       return render_template('delete.html',
#                            title='Home',
#                            form=form,
#                            zu=zu)



 








