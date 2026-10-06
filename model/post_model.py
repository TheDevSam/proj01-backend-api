from database import conectar

def listar_posts():
    conexao = conectar()
    try:
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("""SELECT posts.id, posts.conteudo, posts.criado_em, 
            usuarios.nome, usuarios.username
            FROM posts
            INNER JOIN usuarios ON posts.usuario_id = usuarios.id
            ORDER BY posts.criado_em DESC, posts.id DESC""")

            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conexao.close()