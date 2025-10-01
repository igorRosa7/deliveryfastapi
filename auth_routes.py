from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autentication():
    """
    Essa é a rota de autenticação
    """
    return {"message": "Você acessou a rota de autenticação", "status": False}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha:str, nome: str, session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já existe")
    #raise != return. com return iria retornar sempre 200
    else:
       senha_criptografada = bcrypt_context.hash(senha)
       novo_usuario = Usuario(nome, email, senha_criptografada)
       session.add(novo_usuario)
       session.commit()
       return {"message": f"Usuário criado com sucesso {email}"}
