from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from models import Produto
from database import SessionLocal
from pydantic import BaseModel
from typing import Optional

# Cria a aplicação FastAPI
app = FastAPI()

# Modelo Pydantic para a validação de dados ao criar um produto
class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade_estoque: int = 0

# Função para obter a sessão do banco de dados
async def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Erro no banco de dados")
    finally:
        db.close()

# Endpoint para listar todos os produtos
@app.get("/produtos")
async def listar_produtos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Produto))
    produtos = result.scalars().all()
    return produtos

# Endpoint para criar um novo produto
@app.post("/produtos", status_code=201)
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

# Endpoint para atualizar um produto existente
@app.put("/produtos/{id}")
async def atualizar_produto(
    produto: ProdutoCreate,
    id: int = Path(..., description="ID do produto a ser atualizado"),
    db: AsyncSession = Depends(get_db)
):
    #Busca o produto no banco de dados
    result = await db.execute(select(Produto).where(Produto.id == id))
    produto_existente = result.scalars().first()

    # Verificar se o produto existe
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Atualiza os campos do produto
    produto_existente.nome = produto.nome
    produto_existente.descricao = produto.descricao
    produto_existente.preco = produto.preco
    produto_existente.quantidade_estoque = produto.quantidade_estoque

    # Salva as alterações no banco de dados
    await db.commit()
    await db.refresh(produto_existente)
    return produto_existente

# Endpoint para excluir um produto
@app.delete("/produtos/{id}")
async def excluir_produto(
    id: int = Path(..., description="ID do produto a ser excluído"),
    db: AsyncSession = Depends(get_db)
):
    # Busca o produto no banco de dados
    result = await db.execute(select(Produto).where(Produto.id == id))
    produto_existente = result.scalars().first()

    # Verifica se o produto existe
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Remover o produto do banco de dados
    await db.delete(produto_existente)
    await db.commit()
    return {"message": "Produto excluído com sucesso"}