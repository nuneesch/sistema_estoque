# 📦 Sistema de Controle de Estoque

Este projeto é uma API para gerenciar o estoque de móveis, acessórios e materiais para implantação de projetos em um escritório de arquitetura.

## 🛠 Tecnologias Utilizadas

- **Python 3.9+**
- **FastAPI** (Framework para API)
- **SQLAlchemy + AsyncPG** (Banco de dados PostgreSQL assíncrono)
- **Alembic** (Migração do banco de dados)
- **Pydantic** (Validação de dados)
- **Uvicorn** (Servidor ASGI para rodar o FastAPI)

## 📦 Configuração Inicial do Banco de Dados

Antes de rodar o projeto, você precisa configurar o banco de dados PostgreSQL.

1. **Instale o PostgreSQL**:
   - Siga as instruções no site oficial: [https://www.postgresql.org/download/](https://www.postgresql.org/download/).

2. **Crie o Banco de Dados**:
   - Conecte-se ao PostgreSQL e crie um banco de dados:
     ```bash
     createdb nome_do_banco
     ```

3. **Configure o Arquivo `.env`**:
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
     ```env
     DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/nome_do_banco
     ```
   - Substitua `usuario`, `senha` e `nome_do_banco` pelos valores corretos.

## 🚀 Como Rodar o Projeto Localmente

Siga estas etapas para rodar o projeto no seu ambiente local:

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/sistema_estoque.git
   cd sistema_estoque

2. **Crie um Ambiente Virtual**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instale as Dependências**
    ```bash
    pip install -r requirements.txt

4. **Execute as Migrações do Banco de Dados**
    Se estiver eusando o Alembic, excute:
    ```bash
    alembic upgrade head

5. **Inicie o Servidor**
    ```bash
    uvicorn main:app --reload

6. **Acesse a API**
    A API estará disponível em http://localhost:8000.
    A documentação interativa (Swagger UI) estará disponível em http://localhost:8000/docs


## 📂 Estrutura do Projeto

Aqui está a estrutura do projeto:

sistema_estoque/
├── .env                  # Variáveis de ambiente
├── config.py             # Configurações do projeto
├── database.py           # Configuração do banco de dados
├── main.py               # Ponto de entrada da aplicação
├── models.py             # Modelos do banco de dados
├── README.md             # Documentação do projeto
├── requirements.txt      # Lista de dependências
└── alembic/              # Migrações do banco de dados (se estiver usando Alembic)

## Endpoints da API

A API oferece os seguintes endpoints

Produtos
    GET /produtos: Lista todos os produtos.

    GET /produtos/{id}: Retorna os detalhes de um produto específico.

    POST /produtos: Cria um novo produto.

    PUT /produtos/{id}: Atualiza um produto existente.

    DELETE /produtos/{id}: Exclui um produto.

## Exemplo de Requisição

Criar um Produto:
```json
    {
  "nome": "Cadeira Gamer",
  "descricao": "Cadeira ergonômica para gamers",
  "preco": 1200.0,
  "quantidade_estoque": 10
}

# Como contribuir

1. Faça um fork do Repositório

2. Crie um branch para a sua feature ou correção:
    ```bash
   git checkout -b minha-feature 

3. Faça um commit das Alterações:
    ```bash
    git commit -m "Adiciona nova feature"

4. Envie as Alterações:
    ```bash
    git push origin minha-feature

5. Abra um Pull Request no repositório original

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE] para mais detalhes.