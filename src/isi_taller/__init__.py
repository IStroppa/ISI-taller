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



@app.route('/')
def index():
    return 'index'



@app.route('/login')
def login():
    return 'login'



@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'



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

    if username in USER_DATABASE:
        return f"""
            <h1>Login</h1>
            <p>Username: {username}</p>
            <p>Password: {password}</p>
        """
    else:
        return "Fail"
    

def show_the_login_form():
    return """
        <h1>Login</h1>

        <form method="POST">
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
