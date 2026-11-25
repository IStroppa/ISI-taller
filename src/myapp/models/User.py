from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .RoleType import RoleType

if TYPE_CHECKING:
    from .Question import Question
    from .Response import Response


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    _username: Mapped[str] = mapped_column(
        "username", String(50), nullable=False, unique=True
    )
    _email: Mapped[str] = mapped_column(
        "email", String(100), nullable=False, unique=True
    )
    _password: Mapped[str] = mapped_column("password", String(100), nullable=False)
    _role: Mapped[RoleType] = mapped_column(
        "role", nullable=False, default=RoleType.general_user
    )
    _questions: Mapped[list["Question"]] = relationship(back_populates="_user")

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        role: RoleType = RoleType.general_user,
    ):
        self._username = username
        self._email = email
        self._password = password
        self._role = role

    def get_username(self) -> str:
        return self._username

    def get_role(self) -> RoleType:
        return self._role

    def get_id(self) -> int:
        return self.id
    
    # Añade response a la lista de respuestas de question
    def respond(self, question: "Question", response: "Response"):
        question.add_response(response)