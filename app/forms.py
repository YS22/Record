 # -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, BooleanField,PasswordField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Regexp,EqualTo
from .models import User

class LoginForm(Form):
	username = StringField(u'用户名:', validators=[DataRequired()])
	password = PasswordField(u'密码:', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField(u'登录')

class AdminForm(Form):
	username = StringField(u'用户名:', validators=[DataRequired()])
	password = PasswordField(u'密码:', validators=[DataRequired()])
	reppassword=PasswordField(u'重复密码:', validators=[DataRequired()])
	submit = SubmitField(u'添加')

class QueryForm(Form):
	number=StringField()
	starttime=StringField()
	stoptime=StringField()
	startnumber=StringField()
	stopnumber=StringField()
	testTool=StringField()
	submit = SubmitField(u'Query')
	
