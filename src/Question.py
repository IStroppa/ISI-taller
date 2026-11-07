from datetime import datetime


class Question():
    def __init__(self, tittle: str, body: str):
        self.tittle = tittle
        self.body = body
        self.date = datetime.now()
        self.tags = []

    def mostrar_pregunta(self):
        print(f"Titulo: {self.tittle}")
        print(f"Body: {self.body}")
        