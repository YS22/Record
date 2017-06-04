# -*- coding: utf-8 -*-
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from flask.ext.admin import Admin

# from flask.ext.admin.contrib.sqla import ModelView

app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app,name = u'后台管理系统')
# admin.add_view(MyView(name='Hello'))
# admin.add_view(ModelView(User, db.session))


lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

lm = LoginManager()
lm.init_app(app)
# lm.login_view = 'http://162.243.128.84:90/login'
lm.login_view = 'login'

from app import views,models