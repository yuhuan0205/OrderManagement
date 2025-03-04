from fastapi import FastAPI
from api.dependencies.dependencies import init_db
from api.routers import orders_router

init_db()

app = FastAPI()
app.include_router(orders_router.router)