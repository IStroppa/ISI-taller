from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .Question import Question


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    _questions: Mapped[list["Question"]] = relationship(
        back_populates="_category", cascade="all, delete-orphan"
    )

    _name: Mapped[str] = mapped_column("name", String(100), nullable=False, unique=True)

    def __init__(self, name: str):
        self._name = name

    def get_category_name(self) -> str:
        return self._name

    def set_category_name(self, name: str):
        self._name = name
