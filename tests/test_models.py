import pytest
from sqlalchemy.exc import IntegrityError

from myapp.models.AuthorType import AuthorType
from myapp.models.Category import Category
from myapp.models.Question import Question
from myapp.models.Response import Response
from myapp.models.RoleType import RoleType
from myapp.models.User import User


def test_user_defaults_to_general_user(db):
    user = User("facu", "facu@example.com", "hash")
    db.add(user)
    db.commit()

    assert user.id is not None
    assert user.get_username() == "facu"
    assert user.get_id() == user.id
    assert user.get_role() is RoleType.general_user


def test_user_can_be_admin(db):
    user = User("root", "root@example.com", "hash", RoleType.admin)
    db.add(user)
    db.commit()

    assert user.get_role() is RoleType.admin


def test_question_links_user_category_and_response(db):
    user = User("facu", "facu@example.com", "hash")
    category = Category("Python")
    question = Question("Titulo", "Cuerpo", category, user)
    response = Response("Respuesta", 1, AuthorType.user, question)

    db.add_all([user, category, question, response])
    db.commit()

    assert question._user is user
    assert question._category is category
    assert user._questions == [question]
    assert category._questions == [question]
    assert response in question._responses
    assert response.get_body() == "Respuesta"
    assert response._autType is AuthorType.user
    assert response._accepted is False


def test_unique_username_and_email(db):
    db.add(User("dup", "dup@example.com", "hash"))
    db.commit()

    db.add(User("dup", "otro@example.com", "hash"))
    with pytest.raises(IntegrityError):
        db.commit()
