from flask import Blueprint
from model.usuario_model import listar_usuarios, buscar_perfil, buscar_usuarios

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/api/usuarios")
def obter_usuarios():
    return {"usuarios": listar_usuarios()}


@usuarios_bp.route("/api/usuarios/<string:username>")
def obter_perfil(username):
    perfil = buscar_perfil(username)

    if perfil is None:
        return {"erro": "Usuário não encontrado."}, 404

    return perfil

@usuarios_bp.route("/api/usuarios/busca/<string:termo>")
def pesquisar_usuarios(termo):
    usuarios = buscar_usuarios(termo)
    return {"usuarios": usuarios}
