from flask import Flask, render_template
from controllers.posts_controller import posts_bp
from controllers.usuarios_controller import usuarios_bp

app = Flask(__name__)

app.register_blueprint(posts_bp)
app.register_blueprint(usuarios_bp)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/api/status")
def status_api():
    return {"mensagem": "API funcionando", "ativo": True}