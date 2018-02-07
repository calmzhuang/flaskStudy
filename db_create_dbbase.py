from models import dba
import models
import datetime

def create_database(nickname, email):
    u = models.User(nickname= nickname, email = email)
    dba.session.add(u)
    dba.session.commit()

def select_database():
    users = models.User.query.all()
    for u in users:
        print(u.id, u.nickname)

def insert_blog():
    u = models.User.query.get(1)
    p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)
    dba.session.add(p)
    dba.session.commit()

def delete_data():
    users = models.User.query.all()
    for u in users:
        dba.session.delete(u)

    posts = models.Post.query.all()
    for p in posts:
        dba.session.delete(p)

    dba.session.commit()