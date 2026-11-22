from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .AuthorType import AuthorType

if TYPE_CHECKING:
    from .Question import Question


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    _body: Mapped[str] = mapped_column("body", Text, nullable=False)
    _date: Mapped[datetime] = mapped_column(
        "date", DateTime, default=datetime.now, nullable=False
    )
    _accepted: Mapped[bool] = mapped_column(
        "accepted", Boolean, default=False, nullable=False
    )
    _autID: Mapped[int] = mapped_column("autID", Integer, nullable=False)
    _autType: Mapped[AuthorType] = mapped_column("autType", nullable=False)
    _question_id: Mapped[int] = mapped_column(
        "question_id", ForeignKey("questions.id"), nullable=False
    )
    _question: Mapped["Question"] = relationship(back_populates="_responses")

    def __init__(
        self, body: str, autID: int, autType: AuthorType, question: "Question"
    ):
        self._body = body
        self._date = datetime.now()
        self._accepted = False
        self._autID = autID
        self._autType = autType
        self._question = question

    def get_body(self) -> str:
        return self._body
