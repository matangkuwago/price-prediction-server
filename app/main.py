from fastapi import FastAPI
from app.routers import models, predict, results


app = FastAPI()


app.include_router(models.router, prefix='/models')
app.include_router(predict.router, prefix='/predict')
app.include_router(results.router, prefix='/results')
