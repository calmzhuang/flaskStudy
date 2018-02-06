from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
dba = SQLAlchemy(app)

class User(dba.Model):
    id = dba.Column(dba.Integer, primary_key = True)
    nickname = dba.Column(dba.String(64), index = True, unique = True)
    email = dba.Column(dba.String(120), index = True, unique = True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
