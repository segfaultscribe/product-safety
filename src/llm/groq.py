import httpx
from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

async def query_groq(product_summary: str, user_question: str) -> str:
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        print("GROQ_API_KEY:", GROQ_API_KEY)
        if(not GROQ_API_KEY):
              return "Wont Work!"
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful nutrition assistant. Answer questions about food products based only on the provided information."},
                {"role": "user", "content": f"PRODUCT INFORMATION:\n{product_summary}"},
                {"role": "user", "content": user_question}
            ],
            # "temperature": 0.4,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
