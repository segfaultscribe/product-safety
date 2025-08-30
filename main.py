from fastapi import FastAPI
from src.api.products import ProductsRouter
from dotenv import load_dotenv
 
app = FastAPI()

load_dotenv()

@app.get("/api")
async def root():
    return {"message": "Welcome to Product-safety!"}

app.include_router(ProductsRouter, prefix="/api/products", tags=["products"])
