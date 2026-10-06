-- ============================================================
-- PROJETO: Micro-blogging estilo Twitter
-- BANCO: posts_app
-- SGBD: MySQL
-- ============================================================
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS posts_app
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE posts_app;

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    bio VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE KEY uk_usuarios_username (username)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE posts (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    conteudo VARCHAR(280) NOT NULL,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT fk_posts_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_posts_criado_em
    ON posts (criado_em);

INSERT INTO usuarios (nome, username, bio)
VALUES
('Pedro Viana', 'pedro', 'Estudante de Sistemas de Informação'),
('Ana Silva', 'ana', 'Estudante de tecnologia');

INSERT INTO posts (usuario_id, conteudo)
VALUES
(1, 'Meu primeiro post no projeto!'),
(2, 'Oi pessoal, esse é meu primeiro post!'),
(1, 'Estou aprendendo banco de dados.'),
(2, 'Estou aprendendo Flask também.');

-- CONSULTAS DE TESTE

-- Todos os usuários
SELECT * FROM usuarios;

-- Todos os posts
SELECT * FROM posts;

-- Posts com seus autores
SELECT
    posts.id,
    usuarios.nome,
    usuarios.username,
    posts.conteudo,
    posts.criado_em
FROM posts
INNER JOIN usuarios
    ON posts.usuario_id = usuarios.id
ORDER BY posts.criado_em DESC;

-- Buscar posts pela palavra Flask
SELECT
    posts.id,
    usuarios.nome,
    usuarios.username,
    posts.conteudo,
    posts.criado_em
FROM posts
INNER JOIN usuarios
    ON posts.usuario_id = usuarios.id
WHERE posts.conteudo LIKE '%Flask%'
ORDER BY posts.criado_em DESC;

-- Buscar usuário por nome ou username
SELECT
    id,
    nome,
    username,
    bio
FROM usuarios
WHERE nome LIKE '%Pedro%'
   OR username LIKE '%pedro%';

-- Perfil de um usuário com seus posts
SELECT
    usuarios.id AS usuario_id,
    usuarios.nome,
    usuarios.username,
    usuarios.bio,
    posts.id AS post_id,
    posts.conteudo,
    posts.criado_em
FROM usuarios
LEFT JOIN posts
    ON posts.usuario_id = usuarios.id
WHERE usuarios.username = 'pedro'
ORDER BY posts.criado_em DESC;

-- Exemplo de paginação
SELECT
    posts.id,
    usuarios.username,
    posts.conteudo,
    posts.criado_em
FROM posts
INNER JOIN usuarios
    ON posts.usuario_id = usuarios.id
ORDER BY posts.criado_em DESC
LIMIT 10 OFFSET 0;
