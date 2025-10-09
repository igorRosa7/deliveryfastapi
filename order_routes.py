from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import PedidoSchema 
from models import Pedido

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def list_orders():
    """
    Essa é a rota de pedidos. Todas as rotas de pedidos necessitam de autenticação.
    """
    return {"message": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(get_session)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario) 
    session.add(novo_pedido)
    session.commit()
    return {"mesage": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}