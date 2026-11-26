import os

import pytest

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_EMAIL"] = "admin@example.com"
os.environ["ADMIN_PASSWORD"] = "administradorPrincipal"
os.environ["SECRET_KEY"] = "test-secret"


@pytest.fixture
def app():
    from isi_taller import app as flask_app

    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def reset_db():
    from myapp.database import Base, engine, init_db

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()


@pytest.fixture
def db(reset_db):
    from myapp.database import SessionLocal

    with SessionLocal() as session:
        yield session


@pytest.fixture
def client(app, reset_db):
    return app.test_client()


@pytest.fixture
def logged_in_client(client):
    client.post(
        "/register",
        data={
            "username": "facu",
            "email": "facu@example.com",
            "password": "secreto",
        },
    )
    client.post("/login", data={"username": "facu", "password": "secreto"})
    return client
