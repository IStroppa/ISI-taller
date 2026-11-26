from sqlalchemy import select
from werkzeug.security import check_password_hash

from myapp.models.User import User


def register(client, username="facu", email="facu@example.com", password="secreto"):
    return client.post(
        "/register",
        data={"username": username, "email": email, "password": password},
    )


def test_register_creates_user(client, db):
    response = register(client)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

    user = db.scalar(select(User).where(User._username == "facu"))
    assert user is not None
    assert user._email == "facu@example.com"
    assert user._password != "secreto"
    assert check_password_hash(user._password, "secreto")


def test_register_rejects_missing_fields(client):
    response = client.post(
        "/register", data={"username": "", "email": "", "password": ""}
    )

    assert response.status_code == 200
    assert b"Todos los campos son obligatorios" in response.data


def test_register_rejects_duplicate_username(client):
    register(client)
    response = register(client, email="otro@example.com")

    assert response.status_code == 200
    assert b"El username ya existe" in response.data


def test_register_rejects_duplicate_email(client):
    register(client)
    response = register(client, username="otro")

    assert response.status_code == 200
    assert b"El email ya existe" in response.data


def test_register_and_login_with_special_password(client, db):
    password = "a&b'c"
    register(client, password=password)

    user = db.scalar(select(User).where(User._username == "facu"))
    assert user._username == "facu"
    assert check_password_hash(user._password, password)

    response = client.post("/login", data={"username": "facu", "password": password})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_with_valid_credentials_sets_session(client):
    register(client)

    response = client.post("/login", data={"username": "facu", "password": "secreto"})

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    hub = client.get("/")
    assert b"Bienvenido, facu" in hub.data
    with client.session_transaction() as session:
        assert session["username"] == "facu"


def test_login_with_invalid_credentials(client):
    response = client.post("/login", data={"username": "facu", "password": "malo"})

    assert response.status_code == 200
    assert b"usuario o contrasenia invalida" in response.data
    with client.session_transaction() as session:
        assert "username" not in session


def test_logout_clears_session(client):
    register(client)
    client.post("/login", data={"username": "facu", "password": "secreto"})

    response = client.get("/logout")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    with client.session_transaction() as session:
        assert "username" not in session
