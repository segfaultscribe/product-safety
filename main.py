from fastapi import FastAPI
from src.api.products import ProductsRouter
from dotenv import load_dotenv
 
app = FastAPI()

load_dotenv()

@app.get("/")
async def root():
    return {"message": "Welcome to ProdWise!"}

app.include_router(ProductsRouter, prefix="/products", tags=["products"])
