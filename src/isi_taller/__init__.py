import secrets

from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape  #escapar para tratar a todos lo usuarios como "peligroso"
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from myapp.database import close_db, get_db, init_db
from myapp.models.RoleType import RoleType
from myapp.models.User import User
from myapp.models.Question import Question
from myapp.models.Category import Category

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

init_db()
app.teardown_appcontext(close_db)


# Ruta base del sistema. Muestra el "hub" del servidor, con opciones
# para logearse, registrarse y postear una pregunta con su categoria
@app.route("/")
def app_hub():
    if 'username' in session:
        return render_template('hub.html', username=session['username'])
    return render_template('hub.html')


# Función que define si un login es valido (es decir: el username
# dado está en el sistema, y la contraseña dada le corresponde)
def valid_login(username, password):
    db = get_db()
    user = db.scalar(select(User).where(User._username == username))
    return bool(user and check_password_hash(user._password, password))

# Muestra el formulario para registrar una cuenta nueva en el sistema
@app.get('/register')
def register_get():
    return render_template('register.html')


# Envia el formulario para crear una nueva cuenta
@app.post('/register')
def register_post():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not username or not email or not password:
        return render_template('register.html', error='Todos los campos son obligatorios')

    db = get_db()
    if db.scalar(select(User).where(User._username == username)):
        return render_template('register.html', error='El username ya existe')
    if db.scalar(select(User).where(User._email == email)):
        return render_template('register.html', error='El email ya existe')

    user = User(username, email, generate_password_hash(password), RoleType.general_user)
    db.add(user)
    db.commit()
    return redirect(url_for('login_get'))


# Muestra el formulario para iniciar sesion
@app.get('/login')
def login_get():
    if 'username' in session:
        return render_template('login.html', username=session['username'])
    return render_template('login.html')


# Envia el formulario de login, intenta iniciar sesion
# y da un error si no se consigue
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


# Cierra la sesion abierta del usuario
@app.get('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_get'))


# Muestra el formulario para postear una pregunta
@app.get('/ask')
def ask_get():
    if 'username' in session:
        return render_template('ask.html', username=session['username'])
    return render_template('ask.html')

# Con la informacion recibida del formulario, crea una nueva question
@app.post('/ask')
def ask_post():
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '')
    categoryname = request.form.get('category', '').strip()
    username = request.form.get('user', '').strip()
    
    if not title or not body:
        return render_template('ask.html', error='Uno o mas campos obligatorios faltantes')

    db = get_db()

    user = db.execute(
        select(User).where(User._username == username)
    ).scalar_one_or_none()
    category = db.execute( 
        select(Category).where(Category._name == categoryname)
    ).scalar_one_or_none()

    if not category:
        category = Category(categoryname)
        db.add(category)
        db.commit()
    if not user:
        return render_template('ask.html', error='User faltante')

    question = Question(title, body, category, user)
    db.add(question)
    db.commit()
    return redirect(url_for('login_get'))


# Rutas triviales o auxiliares

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