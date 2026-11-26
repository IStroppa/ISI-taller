import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from myapp.database import close_db, get_db, init_db
from myapp.models.Category import Category
from myapp.models.Question import Question
from myapp.models.RoleType import RoleType
from myapp.models.User import User

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)

init_db()
app.teardown_appcontext(close_db)


@app.route("/")
def app_hub():
    if "username" in session:
        return render_template("hub.html", username=session["username"])
    return render_template("hub.html")


def valid_login(username, password):
    db = get_db()
    user = db.scalar(select(User).where(User._username == username))
    return bool(user and check_password_hash(user._password, password))


@app.get("/register")
def register_get():
    return render_template("register.html")


@app.post("/register")
def register_post():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not username or not email or not password:
        return render_template("register.html", error="Todos los campos son obligatorios")

    db = get_db()
    if db.scalar(select(User).where(User._username == username)):
        return render_template("register.html", error="El username ya existe")
    if db.scalar(select(User).where(User._email == email)):
        return render_template("register.html", error="El email ya existe")

    user = User(username, email, generate_password_hash(password), RoleType.general_user)
    db.add(user)
    db.commit()
    return redirect(url_for("login_get"))


@app.get("/login")
def login_get():
    if "username" in session:
        return render_template("login.html", username=session["username"])
    return render_template("login.html")


@app.post("/login")
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    if valid_login(username, password):
        session["username"] = username
        return redirect(url_for("app_hub"))

    return render_template(
        "login.html",
        error="usuario o contrasenia invalida",
    )


@app.get("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("app_hub"))


@app.get("/ask")
def ask_get():
    if "username" in session:
        return render_template("ask.html", username=session["username"])
    return render_template("ask.html")


@app.post("/ask")
def ask_post():
    if "username" not in session:
        return redirect(url_for("login_get"))

    title = request.form.get("title", "").strip()
    body = request.form.get("body", "")
    categoryname = request.form.get("category", "").strip()

    if not title or not body:
        return render_template(
            "ask.html",
            username=session["username"],
            error="Todos los campos son obligatorios",
        )

    db = get_db()
    user = db.scalar(select(User).where(User._username == session["username"]))
    if user is None:
        session.pop("username", None)
        return redirect(url_for("login_get"))

    category = db.scalar(select(Category).where(Category._name == categoryname))
    if category is None:
        category = Category(categoryname)
        db.add(category)
        db.commit()

    question = Question(title, body, category, user)
    db.add(question)
    db.commit()
    return redirect(url_for("asksuccess"))


@app.route("/asksuccess")
def asksuccess():
    return render_template("asksuccess.html")
