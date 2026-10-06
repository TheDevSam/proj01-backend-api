# API de posts com Flask e MySQL

Aplicação de consulta: lista usuários, mostra perfis e publicações, busca usuários por nome/username e pesquisa conteúdo com paginação de 10 posts.

## Preparação no Windows

Instale Python e MySQL Server, mantenha o serviço MySQL em execução e abra o PowerShell na pasta do projeto.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se já possui um ambiente funcional, não precisa recriá-lo. Ambientes virtuais não devem ser copiados entre computadores.

## Banco de dados

O arquivo banco_twitter.sql cria posts_app, usuarios e posts e insere dois usuários e quatro posts. Ele contém DROP TABLE: uma nova execução apaga os registros existentes nessas tabelas. Não o execute novamente para apenas iniciar a aplicação.

Para a primeira preparação, com o SQL salvo em UTF-8 e SET NAMES utf8mb4 antes das inserções:

```powershell
chcp 65001
mysql --default-character-set=utf8mb4 -u root -p
```

No cliente MySQL (ajuste o caminho se necessário):

```sql
SOURCE C:/Users/Samuel/Documents/proj01-backend-api/banco_twitter.sql;
USE posts_app;
SELECT COUNT(*) FROM usuarios;
SELECT COUNT(*) FROM posts;
exit;
```

Esperado após a carga inicial: 2 e 4. Use seu usuário MySQL caso seja diferente de root.

## Credenciais e execução

No mesmo PowerShell com a .venv ativa:

```powershell
$credencialBanco = Get-Credential -Message "Acesso ao MySQL"
$env:DB_USER = $credencialBanco.UserName
$env:DB_PASSWORD = $credencialBanco.GetNetworkCredential().Password
Remove-Variable credencialBanco
python -m flask --app app run --debug
```

As variáveis valem para essa sessão do terminal. Não grave senhas nos arquivos. database.py usa localhost e posts_app. O modo debug é para desenvolvimento local.

Abra http://127.0.0.1:5000. Para encerrar o servidor, pressione Ctrl+C.

## Organização MVC

- app.py: cria a aplicação, registra os Blueprints e entrega o template.
- database.py: abre a conexão usando as variáveis de ambiente.
- model/: consultas SQL parametrizadas e fechamento de cursor/conexão.
- controllers/: parâmetros HTTP, validação e respostas JSON.
- templates/index.html: formulário, lista, perfil e botões de paginação. JavaScript consome a API com fetch.

## Rotas GET

| Rota | Resultado |
|---|---|
| / | Interface HTML |
| /api/status | Estado da API |
| /api/usuarios | Todos os usuários |
| /api/usuarios/busca/<termo> | Busca por nome ou username |
| /api/usuarios/<username> | Perfil e posts; 404 se inexistente |
| /api/posts | Todos os posts |
| /api/posts/busca/<termo>?pagina=1 | Busca no conteúdo, 10 por página |

As buscas usam LIKE: % e _ têm significado de curingas SQL. Datas DATETIME são devolvidas em ISO sem fuso; este projeto usa horário local. O feed é ordenado por data e ID decrescentes.

## Verificação manual com MySQL

1. Buscar ped e ana na lista; confirmar os perfis correspondentes.
2. Buscar um nome inexistente; confirmar mensagem vazia e botão Mostrar todos.
3. Abrir Pedro e Ana; confirmar dois posts por autor e acentos corretos.
4. Buscar aprendendo no conteúdo; confirmar os dois autores.
5. Buscar conteúdo inexistente; confirmar ausência de resultados.
6. Para testar duas páginas com os poucos registros, mudar temporariamente limite para 1 no posts_controller.py; buscar aprendendo, avançar e voltar. Restaurar limite = 10.
7. Abrir /api/posts/busca/aprendendo?pagina=0 e ?pagina=abc; esperar 400.
8. Abrir /api/usuarios/naoexiste; esperar 404.

Não há login ou rotas de cadastro, edição ou exclusão. Os dados iniciais vêm do SQL. O perfil é exibido na página inicial ao selecionar o usuário.
