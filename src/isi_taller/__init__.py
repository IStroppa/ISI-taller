from flask import Flask, request
from markupsafe import escape #escapar para tratar a todos lo usuarios como "peligroso"
from flask import url_for

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
    return show_the_login_form()



@app.post('/login')
def login_post():
    USER_DATABASE = {
        "admin": "administradorPrincipal",
        "user1": "123456"
    }

    username = request.form.get("username")
    password = request.form.get("password")
    css_url = url_for('static', filename='style.css')


    if username in USER_DATABASE and USER_DATABASE[username] == password:
        return f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Fondo Multicolor</title>
                <link rel="stylesheet" href="{css_url}">
            </head>
            <body>  
                <div class="container">     
                    <h1>Login</h1>
                    <p>Username: {username}</p>
                    <p>Password: {password}</p>
                </div>
            </body>
            </html>
        """
    else:
        return "Fail"
    

def show_the_login_form():
    css_url = url_for("static", filename="style.css")
    return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Login</title>
            <link rel="stylesheet" href="{css_url}">
        </head>
        <body>
            <form method="POST">
                <h1>Login</h1>

                <label>
                    Username:
                    <input type="text" name="username">
                </label>

                <br><br>

                <label>
                    Password:
                    <input type="password" name="password">
                </label>

                <br><br>

                <button type="submit">
                    Login
                </button>
            </form>
        </body>
        </html>
    """

def do_the_login():
    username = request.form.get("username")
    password = request.form.get("password")

    return f"""
        <h1>Login</h1>
        <p>Username: {username}</p>
        <p>Password: {password}</p>
    """



#para ver la ruta absoluta
#with app.test_request_context():
#    print(url_for('index'))
#    print(url_for('login'))
#    print(url_for('login', next='/'))
#    print(url_for('profile', username='John Doe'))
