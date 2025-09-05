from fastapi import APIRouter, Request
from src.api.off import off_api
from src.llm.groq_client import query_groq
from src.helper.format_product import format_product_summary
from src.helper.context import save_product_info, get_history
from pydantic import BaseModel
import json

class ChatRequest(BaseModel):
    question: str
    product: str

ProductsRouter = APIRouter()

@ProductsRouter.get('/find')
async def getProdInformation(request: Request, barcode: str = None):
    session_id = request.cookies.get("session_id")
    if barcode:
        response = off_api.product.get(barcode, fields=[
            'product_name',
            'category_properties',
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
            formatted_response = format_product_summary(response)
            display_result = formatted_response.get("display_result", "")
            assistant_context = formatted_response.get("assistant_context", {})

            print(f"Display_result: {display_result}")
            existing_history = get_history(session_id, barcode)
            if not existing_history:  # only save once
                save_product_info(session_id, barcode, "system", f"PRODUCT INFORMATION:\n{assistant_context}")

            # print(f"response in json: {response}")
            return {
                "display_result": display_result,
                "assistant_context": assistant_context
            }
    else:
        return {"error": "Please provide a name or barcode"}

@ProductsRouter.post('/chat-with-item')
async def chat_with_item(request: Request, data: ChatRequest):
    print(data.product)
    session_id = request.cookies.get("session_id")
    summary = get_history(session_id, data.product)
    print(summary)
    # store user message in chat history
    save_product_info(session_id, data.product, "user", f"Question about {data.product}: {data.question}")
    answer = await query_groq(summary, data.question)
    print(f"SUMMARY: {summary}, QUESTION:{data.question}")
    # store assistant reply
    save_product_info(session_id, data.product, "assistant", answer)
    return {
        "answer": answer,
        "messages": get_history(session_id, data.product),
        "session_id": session_id
    }
