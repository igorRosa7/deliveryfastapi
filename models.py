from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType ##possibilita criar campos com escolhas, como um type ou interface, enum.. mas é uma tupla


#cria conexao
db = create_engine("sqlite:///banco.db")
#cria base -- ver sobre isso
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True )
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

 #   STATUS_PEDIDOS = (
 #      ("PENDENTE", "PENDENTE"),
 #     ("CANCELADO", "CANCELADO"),
 #    ("FINALIZADO", "FINALIZADO"),
 # )
 #troquei ChoiceType(choices=STATUS_PEDIDOS) por String pq tava dando erro no alembic migration. 
 #Deletei o arquivo de versão, o arquivo de versao do cache e o banco e criei tudo de novo.
 #Se quiser usar o ChoiceType, tem que criar a migration manualmente.
 #alemc revision --autogenerate -m "...." para editar a versão // sempre que editar o BD e foi fazer a migration, realiza esse processo
 #funciona como um versionamento do git
 #alembic upgrade head para aplicar a migration

    id = Column("id", Integer, primary_key=True, autoincrement=True )
    status = Column("status", String)
    usuario = Column("usuario",ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    #itens...
  
    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

class ItensPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True )
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido