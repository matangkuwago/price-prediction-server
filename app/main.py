from fastapi import FastAPI
from app.routers import predict, get_results


app = FastAPI()


app.include_router(predict.router, prefix='/predict')
app.include_router(get_results.router, prefix='/get_results')
