from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base  # Importa a base de modelos
import asyncio
from config import DATABASE_URL

# Cria a engine do banco de dados (conexão assíncrona)
engine = create_async_engine(DATABASE_URL, echo=True)

# Configura a sessão do banco de dados
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Função para criar as tabelas no banco de dados
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")

# Executa a função assíncrona para criar as tabelas
if __name__ == "__main__":
    asyncio.run(init_db())