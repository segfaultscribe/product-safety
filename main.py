from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from src.api.products import ProductsRouter
from dotenv import load_dotenv
import uuid
 
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

# middleware to add session cookie to each user, we'll need to rate limit em'
@app.middleware("http")
async def add_session_cookie(request: Request, call_next):
    response: Response = await call_next(request)
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="Lax"
        )
    return response

app.include_router(ProductsRouter, prefix="/api/products", tags=["products"])

@app.get("/api")
async def root():
    return {"message": "Welcome to Product-safety!"}


