from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    token = f"fdkfjsçdlfgg{id_usuario}"
    return token


@auth_router.get("/")
async def autentication():
    """
    Essa é a rota de autenticação
    """
    return {"message": "Você acessou a rota de autenticação", "status": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session:Session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já existe")
    #raise != return. com return iria retornar sempre 200
    else:
       senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
       novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
       session.add(novo_usuario)
       session.commit()
       return {"message": f"Usuário criado com sucesso {usuario_schema.email}"}

#login -> email e senha -> token JWT (Json Web Token) -> rota protegida
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token,
                "token_type": "bearer"
                }
    #JWT Bearer
        