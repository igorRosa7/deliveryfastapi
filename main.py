from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


# roda uma vez que sobe a app e vai atualizando. é tipo um npm run dev do packeage.
# uvicorn main:app --reload


