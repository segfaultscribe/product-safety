from fastapi import FastAPI
from api.products import ProductsRouter
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to ProdWise!"}

app.include_router(ProductsRouter, prefix="/products", tags=["products"])
