from database import conectar


def listar_posts():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT posts.id, posts.conteudo, posts.criado_em,
                   usuarios.nome, usuarios.username
            FROM posts
            INNER JOIN usuarios ON posts.usuario_id = usuarios.id
            ORDER BY posts.criado_em DESC, posts.id DESC
        """)

        posts = cursor.fetchall()

        for post in posts:
            post["criado_em"] = post["criado_em"].isoformat()

        return posts
    finally:
        if cursor is not None:
            cursor.close()


def buscar_posts(termo, limite, offset):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT posts.id, posts.conteudo, posts.criado_em,
                   usuarios.nome, usuarios.username
            FROM posts
            INNER JOIN usuarios ON posts.usuario_id = usuarios.id
            WHERE posts.conteudo LIKE %s
            ORDER BY posts.criado_em DESC, posts.id DESC
            LIMIT %s OFFSET %s
        """, (f"%{termo}%", limite, offset))

        posts = cursor.fetchall()

        for post in posts:
            post["criado_em"] = post["criado_em"].isoformat()

        return posts
    finally:
        if cursor is not None:
            cursor.close()