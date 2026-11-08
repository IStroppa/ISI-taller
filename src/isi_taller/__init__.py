from flask import Flask, request
from markupsafe import escape #escapar para tratar a todos lo usuarios como "peligroso"
from flask import url_for
from flask import render_template

app = Flask(__name__)


@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'



@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'



@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'



@app.route('/projects/')
def projects():
    return 'The project page'



@app.route('/about')
def about():
    return 'The about page'



@app.get('/login')
def login_get():
    return render_template('login.html')



@app.post('/login')
def login_post():
    USER_DATABASE = {
        "admin": "administradorPrincipal",
        "user1": "123456"
    }

    username = request.form.get("username")
    password = request.form.get("password")


    if username in USER_DATABASE and USER_DATABASE[username] == password:
        return render_template('login.html', username=username, password=password)
    else:
        return "Fail"
    
