import secrets

from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape  #escapar para tratar a todos lo usuarios como "peligroso"

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

def valid_login(username, password):
    USER_DATABASE = {
        "admin": "administradorPrincipal",
        "user1": "123456"
    }

    return bool(username in USER_DATABASE and USER_DATABASE[username] == password)

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
    if 'username' in session:
        return render_template('login.html', username=session['username'])
    return render_template('login.html')



@app.post('/login')
def login_post():
    error = None 
    username = request.form.get("username")
    password = request.form.get("password")


    if valid_login(username, password):
            session['username'] = username
            return render_template('login.html', username=username)
    else:
        error = 'usuario o contrasenia invalida'
        return render_template('login.html', error=error)



@app.get('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_get'))