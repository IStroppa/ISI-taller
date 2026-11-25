from sqlalchemy import inspect, select
from werkzeug.security import check_password_hash

from myapp.database import ADMIN_PASSWORD, ADMIN_USERNAME, engine
from myapp.models.User import User


def test_init_db_creates_tables_and_admin(db):
    tables = set(inspect(engine).get_table_names())
    assert {"users", "categories", "questions", "responses"} <= tables

    admin = db.scalar(select(User).where(User._username == ADMIN_USERNAME))
    assert admin is not None
    assert admin.get_role().name == "admin"
    assert admin._password != ADMIN_PASSWORD
    assert check_password_hash(admin._password, ADMIN_PASSWORD)
