from flask import g
from sqlalchemy import text

from myapp.database import get_db


def test_get_db_reuses_session_and_teardown_closes_it(app):
    with app.test_request_context("/login"):
        first = get_db()
        first.execute(text("SELECT 1"))
        assert first is get_db()
        assert g.db is first
        assert first.in_transaction()

    assert not first.in_transaction()
