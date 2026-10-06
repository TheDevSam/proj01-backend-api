from flask import Blueprint
from model.usuario_model import listar_usuarios, buscar_perfil

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