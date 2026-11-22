"""users responses and question author

Revision ID: f3ced681ea97
Revises: 0001_initial_schema
Create Date: 2026-11-22 15:29:38.654443
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f3ced681ea97"
down_revision: str | None = "0001_initial_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column(
            "role",
            sa.Enum("general_user", "admin", name="roletype"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "responses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=False),
        sa.Column("autID", sa.Integer(), nullable=False),
        sa.Column(
            "autType",
            sa.Enum("ai", "user", name="authortype"),
            nullable=False,
        ),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("questions", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "fk_questions_user_id_users", "users", ["user_id"], ["id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("questions", schema=None) as batch_op:
        batch_op.drop_constraint("fk_questions_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")

    op.drop_table("responses")
    op.drop_table("users")
