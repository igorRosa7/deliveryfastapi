from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def list_orders():
    """
    Essa é a rota de pedidos. Todas as rotas de pedidos necessitam de autenticação.
    """
    return {"message": "Você acessou a rota de pedidos"}