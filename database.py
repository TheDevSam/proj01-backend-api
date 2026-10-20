# database.py
import os
import mysql.connector
from flask import g


def conectar():
    if "conexao" not in g:
        g.conexao = mysql.connector.connect(
            host="localhost",
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database="posts_app"
        )
    return g.conexao


def fechar_conexao(exception=None):
    conexao = g.pop("conexao", None)
    if conexao is not None:
        conexao.close()


def inicializar_banco(app):
    app.teardown_appcontext(fechar_conexao)