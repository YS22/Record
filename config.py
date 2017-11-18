# _*_coding:utf8 _*_
import os
import socket

basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'mysql://root:1234pttK@47.93.103.136:3306/test?charset=utf8'

hostname = socket.gethostname()
if hostname == 'chalinandeMac-mini.local': #开发环境
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/test?charset=utf8'

if hostname == 'iZ2ze7ry8wsws4xlrloit3Z':  #生产环境
	SQLALCHEMY_DATABASE_URI = 'mysql://root:1234pttK@127.0.0.1:3306/test?charset=utf8'

if hostname == 'HANZHENG':   #Linksame
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'