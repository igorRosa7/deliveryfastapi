from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autentication():
    """
    Essa é a rota de autenticação
    """
    return {"message": "Você acessou a rota de autenticação", "status": False}
