from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #se o scheme bcrypt ficar obsoleto, ele escolhe um novo

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


# roda uma vez que sobe a app e vai atualizando. é tipo um npm run dev do packeage.
# uvicorn main:app --reload


