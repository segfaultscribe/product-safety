from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.products import ProductsRouter
from dotenv import load_dotenv
 
app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

load_dotenv()

@app.get("/api")
async def root():
    return {"message": "Welcome to Product-safety!"}

app.include_router(ProductsRouter, prefix="/api/products", tags=["products"])
