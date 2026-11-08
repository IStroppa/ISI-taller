from datetime import datetime

from .Category import Category


class Question:
    def __init__(self, title: str, body: str, category: Category):
        self._title = title
        self._body = body
        self._date = datetime.now()
        self._tags = []
        self._category = category    

    def mostrar_pregunta(self):
        print(f"Titulo: {self._title}")
        print(f"Body: {self._body}")
        print(f"Category: {self._category.get_category_name()}")
        