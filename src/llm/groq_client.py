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
                {"role": "system",
                    "content": """
                    You are a Nutrition Assistant that explains food product information clearly and helpfully. 
                    Do not use markdown format, output in plain text only
                    Be clear, natural, and engaging. 
                    You may give practical dietary suggestions if safe, but avoid making medical claims. 
                    Keep it under 500 characters unless explanation requires extra clarity.

                    Guidelines:
                    - Base answers on the provided product data first and foremost.
                    - You may add **helpful, low-risk context** (e.g., typical serving advice, why high sugar matters), but always clarify when it's general knowledge vs. product-specific.
                    - If something is not stated in the data, say so directly instead of guessing exact values.
                    - For dietary follow-ups, give thoughtful, human-like explanations that highlight concerns (e.g., sugar, fat, allergens).
                    - If the question is unrelated to nutrition or food products, respond with: 
                    "I'm a food assistant and cannot help with that."
                    - Aim for responses that are detailed, engaging, and natural in tone—like you’re talking to a curious person, not just listing facts.
                    - Keep responses under 700 characters (concise but not overly strict).
                    - Use plain text and natural sentences, not just fragments.
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
