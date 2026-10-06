from database import conectar


def listar_usuarios():
    conexao = conectar()
    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, username
            FROM usuarios
            ORDER BY nome, id
        """)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()


def buscar_perfil(username):
    conexao = conectar()
    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nome, username, bio
            FROM usuarios
            WHERE username = %s
        """, (username,))

        usuario = cursor.fetchone()

        if usuario is None:
            return None

        cursor.execute("""
            SELECT id, conteudo, criado_em
            FROM posts
            WHERE usuario_id = %s
            ORDER BY criado_em DESC, id DESC
        """, (usuario["id"],))

        posts = cursor.fetchall()

        for post in posts:
            post["criado_em"] = post["criado_em"].isoformat()

        return {"usuario": usuario, "posts": posts}
    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()