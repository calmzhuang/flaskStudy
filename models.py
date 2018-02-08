from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
dba = SQLAlchemy(app)

class User(dba.Model):
    id = dba.Column(dba.Integer, primary_key = True)
    nickname = dba.Column(dba.String(64), index = True, unique = True)
    email = dba.Column(dba.String(120), index = True, unique = True)
    posts = dba.relationship('Post', backref='author', lazy='dynamic')

    dis_authenticated = True

    is_active = True

    is_anonymous = False

    def get_id(self):
        try:
            return str(self.id)
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(dba.Model):
    id = dba.Column(dba.Integer, primary_key = True)
    body = dba.Column(dba.String(140))
    timestamp = dba.Column(dba.DateTime)
    user_id = dba.Column(dba.Integer, dba.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
