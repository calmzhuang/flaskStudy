import os
from flask import render_template, flash, redirect, Flask
os.path.abspath('/forms')
from forms import LoginForm
# from config import DevConfig
import config
from views import app

# app = Flask(__name__)
app.config.from_object(config)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                           title = 'Sign In',
                           form = form,
                           providers = app.config['OPENID_PROVIDERS'])

if __name__ == '__main__':
    app.run()