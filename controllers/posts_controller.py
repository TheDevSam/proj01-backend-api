from flask import Blueprint, request
from model.post_model import listar_posts

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/api/posts/busca/<string:termo>")
def busca_post(termo):
    pagina = request.args.get("pagina", default=1, type=int)
    if pagina < 1:
        return {"erro": "A pagina deve ser maior ou igual a 1."}, 400

    limite = 10
    offset = (pagina - 1) * limite     
    
    return {"termo_pesquisado": termo, "pagina": pagina, "limite": limite, "offset": offset}

@posts_bp.route("/api/posts", methods=["GET"])
def obter_posts():
    posts = listar_posts()
    return {"posts": posts}
