from sqlalchemy import select

from myapp.models.Category import Category
from myapp.models.Question import Question


def test_secret_key_comes_from_environment(app):
    assert app.secret_key == "test-secret"


def test_hub_for_guest(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Bienvenido" in response.data
    assert "Iniciar sesión".encode() in response.data
    assert b"Hacer una pregunta" not in response.data


def test_hub_for_logged_user(logged_in_client):
    response = logged_in_client.get("/")

    assert response.status_code == 200
    assert b"Bienvenido, facu" in response.data
    assert b"Hacer una pregunta" in response.data
    assert "Cerrar sesión".encode() in response.data


def test_login_get_shows_welcome_when_logged_in(logged_in_client):
    response = logged_in_client.get("/login")

    assert response.status_code == 200
    assert b"Bienvenido, facu" in response.data


def test_ask_get_for_guest(client):
    response = client.get("/ask")

    assert response.status_code == 200
    assert b"Acceso no permitido" in response.data


def test_ask_post_requires_login(client):
    response = client.post(
        "/ask",
        data={"title": "Titulo", "body": "Cuerpo", "category": "General"},
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_ask_get_for_logged_user(logged_in_client):
    response = logged_in_client.get("/ask")

    assert response.status_code == 200
    assert b"Publicar nueva pregunta" in response.data


def test_ask_creates_question_and_category(db, logged_in_client):
    response = logged_in_client.post(
        "/ask",
        data={
            "title": "Como testear",
            "body": "Quiero probar el formulario",
            "category": "Testing SQL",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/asksuccess")

    category = db.scalar(select(Category).where(Category._name == "Testing SQL"))
    question = db.scalar(select(Question).where(Question._title == "Como testear"))
    assert category is not None
    assert question is not None
    assert question._body == "Quiero probar el formulario"
    assert question._category._name == "Testing SQL"
    assert question._user._username == "facu"


def test_ask_success_page_shows_waiting(logged_in_client):
    response = logged_in_client.get("/asksuccess")

    assert response.status_code == 200
    assert b"Esperando respuesta" in response.data


def test_ask_rejects_incomplete_form(logged_in_client):
    response = logged_in_client.post(
        "/ask",
        data={"title": "", "body": "", "category": "General"},
    )

    assert response.status_code == 200
    assert b"Todos los campos son obligatorios" in response.data
