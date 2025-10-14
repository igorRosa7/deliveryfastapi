from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import get_session, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao} #sub = dono to token, id do usuario
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario



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
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha inválida")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) #token de 7 dias
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }
    #JWT Bearer

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    #verificar token
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
        