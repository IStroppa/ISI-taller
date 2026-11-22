import os

from flask import g
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///isi_taller.db")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "administradorPrincipal")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def init_db():
    from .models.Category import Category
    from .models.Question import Question
    from .models.Response import Response
    from .models.RoleType import RoleType
    from .models.User import User

    _ = (Category, Question, Response, User)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        admin = db.scalar(select(User).where(User._username == ADMIN_USERNAME))
        if admin is None:
            db.add(
                User(
                    ADMIN_USERNAME,
                    ADMIN_EMAIL,
                    generate_password_hash(ADMIN_PASSWORD),
                    RoleType.admin,
                )
            )
            db.commit()


def get_db():
    if "db" not in g:
        g.db = SessionLocal()
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
