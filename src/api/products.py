from fastapi import APIRouter, Request
from src.api.off import off_api
from src.llm.groq_client import query_groq
from src.helper.format_product import format_product_summary
from src.helper.context import save_product_info, get_history
import json

ProductsRouter = APIRouter()

@ProductsRouter.get('/find')
async def getProdInformation(request: Request, barcode: str = None):
    session_id = request.cookies.get("session_id")
    if barcode:
        response = off_api.product.get(barcode, fields=[
            'nutrient_levels', 
            'nutriments', 
            'nutrition_grades_tags', 
            'allergens', 
            'allergens_from_ingredients', 
            'categories', 
            'image_url', 
            'ingredients_hierarchy', 
            'ingredients_text_en_ocr_1642445989_result', 
            'categories_tags', 
            'labels_tags', 
            'traces', 
            'additives_tags', 
            'ecoscore_grade',
            'serving_size',
            'quantity_per_unit',
        ])

        if response:
            # Save ALL the data to a formatted JSON file
            response = format_product_summary(response)
            save_product_info(session_id, "system", f"PRODUCT INFORMATION:\n{response}")
            print(f"response in json: {response}")
            return response
    else:
        return {"error": "Please provide a name or barcode"}

@ProductsRouter.get('/chat-with-item')
async def chat_with_item(request: Request, barcode: str, question: str):
    session_id = request.cookies.get("session_id")
    summary = get_history(session_id)
    # store user message in chat history
    save_product_info(session_id, "user", f"Question about {barcode}: {question}")
    answer = await query_groq(summary, question)
    # store assistant reply
    save_product_info(session_id, "assistant", answer)
    return {
        "answer": answer,
        "messages": get_history(session_id),
        "session_id": session_id
    }
