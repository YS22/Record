import os
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = 'mysql://root:1234pttK@47.93.103.136:3306/test?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1:3306/test?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'