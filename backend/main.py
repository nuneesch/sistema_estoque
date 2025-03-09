from fastapi import FastAPI, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from models import Produto
from database import SessionLocal
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import asyncio

# Garante que o loop de eventos esteja aberto
if not asyncio.get_event_loop().is_running():
    asyncio.set_event_loop(asyncio.new_event_loop())

# Cria a aplicação FastAPI
app = FastAPI()

# Modelo Pydantic para a validação de dados ao criar um produto
class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_lenght=1, max_lenght=100, description="Nome do Produto")
    descricao: Optional[str] = Field(None, max_length=255, description="Descrição do Produto")
    preco: float = Field(..., gt=0, description="Preço do Produto (Deve ser maior que zero)")
    quantidade_estoque: int = Field(0, ge=0, description="Quantidade em Estoque Deve ser maior que zero)")

    # Validação personalizada para o nome
    @field_validator("nome")
    def nome_nao_pode_ser_vazio(cls,value):
        if not value.strip():
            raise ValueError("O Nome do Produto não pode ser vazio")
        return value

# Função para obter a sessão do banco de dados
async def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro no banco de dados")
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
    try:
        #Busca o produto no banco de dados
        result = await db.execute(select(Produto).where(Produto.id == id))
        produto_existente = result.scalars().first()

        # Verificar se o produto existe
        if not produto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Produto não encontrado"
                )
        
        # Atualiza os campos do produto
        produto_existente.nome = produto.nome
        produto_existente.descricao = produto.descricao
        produto_existente.preco = produto.preco
        produto_existente.quantidade_estoque = produto.quantidade_estoque

        # Salva as alterações no banco de dados
        await db.commit()
        await db.refresh(produto_existente)
        return produto_existente
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar o Produto: {str(e)}"
    )


# Endpoint para excluir um produto
@app.delete("/produtos/{id}")
async def excluir_produto(
    id: int = Path(..., description="ID do produto a ser excluído"),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Busca o produto no banco de dados
        result = await db.execute(select(Produto).where(Produto.id == id))
        produto_existente = result.scalars().first()

        # Verifica se o produto existe
        if not produto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Produto não encontrado"
                )
        
        # Remover o produto do banco de dados
        db.delete(produto_existente)
        await db.commit()
        return {"message": "Produto excluído com sucesso"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao excluir o Produto: {str(e)}"
        )