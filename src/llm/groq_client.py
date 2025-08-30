import httpx
from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=GROQ_API_KEY)

async def query_groq(product_summary: str, user_question: str) -> str:
        
        chat_completion = client.chat.completions.create(
            model = GROQ_MODEL,
            messages = [
                {"role": "system", "content": """You are a Nutrition Assistant that provides information strictly based on provided food product data.
                    Rules:
                    Do not assume, infer, or estimate any values that are not explicitly stated in the data.
                    If an answer cannot be determined from the provided data, say so clearly. You may reference packaging standards or general dietary guidelines where appropriate.
                    If the question is unrelated to the food product or dietary follow-ups, reply with:
                    “I'm a food assistant and cannot help with that.”
                    Only say “I'm a food assistant” when responding to completely irrelevant topics (e.g., movies, electronics).
                    If the follow-up is dietary in nature (e.g., portion size, calories, suitability), respond appropriately using only the given data.
                    Keep all responses under 450 characters.
                    Use plain text and standard punctuation only.
                 """},
                {"role": "user", "content": f"PRODUCT INFORMATION:\n{product_summary}"},
                {"role": "user", "content": user_question}
            ],
            # "temperature": 0.4,
        )
        return chat_completion.choices[0].message.content

        # async with httpx.AsyncClient() as client:
        #     response = await client.post(GROQ_API_URL, headers=headers, json=payload)
        #     response.raise_for_status()
        #     return response.json()["choices"][0]["message"]["content"]
