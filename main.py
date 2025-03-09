from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Produto
from database import SessionLocal
from pydantic import BaseModel

# Cria a aplicação FastAPI
app = FastAPI()

# Modelo Pydantic para validação de dados ao criar um produto
class ProdutoCreate(BaseModel):
    nome: str
    descricao: str = None
    preco: float
    quantidade_estoque: int = 0

# Função para obter a sessão do banco de dados
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# Endpoint para listar todos os produtos
@app.get("/produtos")
async def listar_produtos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Produto))
    produtos = result.scalars().all()
    return produtos

# Endpoint para criar um novo produto
@app.post("/produtos")
async def criar_produto(produto: ProdutoCreate, db: AsyncSession = Depends(get_db)):
    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque
    )
    db.add(novo_produto)
    await db.commit()
    await db.refresh(novo_produto)
    return novo_produto