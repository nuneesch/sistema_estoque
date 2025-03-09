# 📦 Sistema de Controle de Estoque

Este projeto é uma API para gerenciar o estoque de móveis, acessórios e materiais para implantação de projetos em um escritório de arquitetura.

## 🛠 Tecnologias Utilizadas

- **Python 3.13**
- **FastAPI** (Framework para API)
- **SQLAlchemy + AsyncPG** (Banco de dados PostgreSQL assíncrono)
- **Alembic** (Migração do banco de dados)

## 📦 Configuração Inicial do Banco de Dados

### Criar Banco de Dados PostgreSQL

1. Abra o terminal e execute:
   ```sh
   psql -U postgres
2. Digite a senha do PostgreSQL
3. Crie o Banco de Dados: 
    CREATE DATABASE estoque_db;
4. Confirme a criação com:
    \l
5. Saia do PostgreSQL:
    \q

    