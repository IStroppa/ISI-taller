from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .Category import Category
from .Response import Response


class Question(Base):
    __tablename__ = "questions"

    # Atributos ocultos de administración
    id: Mapped[int] = mapped_column(primary_key=True)
    _user_id: Mapped[int] = mapped_column(
        "user_id", ForeignKey("users.id"), nullable=False
    )
    _category_id: Mapped[int] = mapped_column(
        "category_id", ForeignKey("categories.id"), nullable=False
    )

    # Atributos a mostrar
    _title: Mapped[str] = mapped_column("title", String(200), nullable=False)
    _body: Mapped[str] = mapped_column("body", Text, nullable=False)
    _date: Mapped[datetime] = mapped_column(
        "date", DateTime, default=datetime.now, nullable=False
    )
    _tags: Mapped[list[str]] = mapped_column("tags", JSON, default=list, nullable=False)
    _category: Mapped[Category] = relationship(back_populates="_questions")
    _responses: Mapped[list[Response]] = relationship(back_populates="_question")



    def __init__(self, title: str, body: str, category: Category):
        self._title = title
        self._body = body
        self._date = datetime.now()
        self._tags = []
        self._category = category
        self._responses = []

    # Imprime la pregunta
    def mostrar_pregunta(self):
        print(f"Titulo: {self._title}")
        print(f"Body: {self._body}")
        print(f"Category: {self._category.get_category_name()}")

    # Añade response a la lista de preguntas
    def add_response(self, response: Response):
        self._responses.append(response)
