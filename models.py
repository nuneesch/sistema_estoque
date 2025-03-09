from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base

# Base declarativa para os modelos SQLAlchemy
Base = declarative_base()

class Produto(Base):
    """Modelo da tabela 'produtos'."""
    __tablename__ = "produtos"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)  # Nome do produto (obrigatório)
    descricao = Column(String(255), nullable=True)  # Descrição (opcional)
    preco = Column(Float, nullable=False)  # Preço (obrigatório)
    quantidade_estoque = Column(Integer, nullable=False, default=0)  # Estoque (default 0)
    data_criacao = Column(DateTime, default=func.now())  # Data de criação automática