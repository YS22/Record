 # -*- coding: utf-8 -*-
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), index = True, unique = True)
    password = db.Column(db.String(30))
    role = db.Column(db.String(60))
    

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Modules(db.Model):

    '''
    29条数据类型
    '''
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(60))
    number = db.Column(db.String(60))
    maxPress = db.Column(db.Integer)
    minPress = db.Column(db.Integer)
    press = db.Column(db.Integer)
    maxPressPosition = db.Column(db.Float)
    minPressPosition = db.Column(db.Float)
    pressPosition = db.Column(db.Float)
    minPressPower = db.Column(db.Float)
    maxPressPower = db.Column(db.Float)
    pressPower = db.Column(db.Float)
    maxPressStroke = db.Column(db.Float)
    minPressStroke = db.Column(db.Float)
    pressStroke = db.Column(db.Float)
    maxBack = db.Column(db.Integer)
    minBcak = db.Column(db.Integer)
    back = db.Column(db.Integer)
    maxBackPosition = db.Column(db.Float)
    minBackPosition = db.Column(db.Float)
    backPosition = db.Column(db.Float)
    minBackPower = db.Column(db.Float)
    maxBackPower = db.Column(db.Float)
    backPower = db.Column(db.Float)
    maxBackStroke = db.Column(db.Float)
    minBackStroke = db.Column(db.Float)
    backStroke = db.Column(db.Float)
    testTime = db.Column(db.DateTime)
    testTool = db.Column(db.String(120))
    #tester=db.Column(db.String(60))