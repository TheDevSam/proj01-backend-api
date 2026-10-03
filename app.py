from flask import Flask
from controllers.posts_controller import posts_bp

app = Flask(__name__)
app.register_blueprint(posts_bp)

@app.route("/")
def inicio():
    return "inicio"

@app.route("/api/status")
def status_api():
    return {"mensagem": "um monte de abobrinha", "ativo": True}