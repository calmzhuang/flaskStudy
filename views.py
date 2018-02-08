from flask import render_template, flash, redirect, session, url_for, request, g
# from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import dba, User, Post
from forms import LoginForm
from flask import Flask
from config import DevConfig, basedir
import os, config
# from flask.ext.openid import OpenID
from flask_openid import OpenID

app = Flask(__name__)
app.config.from_object(DevConfig)
app.config.from_object(config)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index/')
@login_required
def index():
    user = {'nickname': 'Mr.Han'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }]
    return render_template('index.html',
                           title = 'Home',
                           user = user,
                           posts = posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

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
        dba.session.add(user)
        dba.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()