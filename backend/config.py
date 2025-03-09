import os
from dotenv import load_dotenv

# Carrega variaveis de ambiente do arquivo .env (que será criado futuramente)
load_dotenv()

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
