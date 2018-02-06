from flask import render_template
from flask import Flask
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

@app.route('/')
@app.route('/index/')
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

if __name__ == '__main__':
    app.run()