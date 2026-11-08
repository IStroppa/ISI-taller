from flask import Flask, request
from markupsafe import escape #escapar para tratar a todos lo usuarios como "peligroso"

app = Flask(__name__)

@app.route("/hello")
def hello():
        name = request.args.get("name", "Flask")
        return f"Hello, {escape(name)}!"