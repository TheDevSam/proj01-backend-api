from flask import Blueprint, request
from model.post_model import listar_posts, buscar_posts

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/api/posts/busca/<string:termo>")
def busca_post(termo):
    try:
        pagina = int(request.args.get("pagina", "1"))
    except ValueError:
        return {"erro": "A página deve ser um número inteiro."}, 400

    if pagina < 1:
        return {"erro": "A pagina deve ser maior ou igual a 1."}, 400

    limite = 10
    offset = (pagina - 1) * limite
    resultados = buscar_posts(termo, limite + 1, offset)
    tem_proxima = len(resultados) > limite
    posts = resultados[:limite]

    return {
        "termo_pesquisado": termo,
        "pagina": pagina,
        "limite": limite,
        "offset": offset,
        "posts": posts,
        "tem_anterior": pagina > 1,
        "tem_proxima": tem_proxima
    }


@posts_bp.route("/api/posts", methods=["GET"])
def obter_posts():
    posts = listar_posts()
    return {"posts": posts}
