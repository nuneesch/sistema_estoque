from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from config import DATABASE_URL

# Criar um motor de conexão assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Criar uma sessão assíncrona
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def test_connection():
    # Criar uma sessão para garantir o uso adequado
    async with SessionLocal() as session:
        async with session.begin():
            # Usando a consulta select
            result = await session.execute(select(1))
            print("Conexão bem-sucedida:", result.scalar())

# Rodar a função assíncrona para testar a conexão
import asyncio
asyncio.run(test_connection())
