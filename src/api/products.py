from fastapi import APIRouter
from src.api.off import off_api
from src.llm.groq import query_groq

import json

ProductsRouter = APIRouter()


def format_product_summary(data: dict) -> str:
    try:
        # Helper functions
        def get_nutrient(val, unit='g'):
            return f"{val} {unit}" if val is not None else "N/A"
        
        nutrient_levels = data.get("nutrient_levels", {})
        nutriments = data.get("nutriments", {})
        allergens = data.get("allergens", "None listed").replace("en:", "").split(",")
        allergens_from_ingredients = data.get("allergens_from_ingredients", "").split(",")
        categories = data.get("categories", "").replace(",", " > ")
        image_url = data.get("image_url", "")
        ingredients = data.get("ingredients_text_en_ocr_1642445989_result", "No ingredients listed.")

        summary = f"""📦 Product Categories: {categories}

![product-image]({image_url})

🍫 Ingredients:
{ingredients.strip()}

⚠️ Allergens:
- Declared: {', '.join([a.strip() for a in allergens if a.strip()])}
- From Ingredients: {', '.join([a.strip() for a in allergens_from_ingredients if a.strip()])}

🍽️ Nutrient Levels (per 100g):
""" + "\n".join([f"- {k.replace('-', ' ').title()}: {v.title()}" for k, v in nutrient_levels.items()]) + "\n\n"

        summary += f"""🔬 Nutrition Facts (per 100g):
- Calories: {get_nutrient(nutriments.get('energy-kcal_100g'), 'kcal')}
- Energy: {get_nutrient(nutriments.get('energy-kj_100g'), 'kJ')}
- Carbohydrates: {get_nutrient(nutriments.get('carbohydrates_100g'))}
- Sugars: {get_nutrient(nutriments.get('sugars_100g'))}
- Fat: {get_nutrient(nutriments.get('fat_100g'))}
- Saturated Fat: {get_nutrient(nutriments.get('saturated-fat_100g'))}
- Proteins: {get_nutrient(nutriments.get('proteins_100g'))}
- Salt: {get_nutrient(nutriments.get('salt_100g'))}
- Sodium: {get_nutrient(nutriments.get('sodium_100g'))}

🌱 Other Info:
- Fruits/Vegetables/Nuts Estimate: {nutriments.get('fruits-vegetables-nuts-estimate-from-ingredients_100g', 'N/A')}%
- NOVA Group: {nutriments.get('nova-group', 'N/A')} (Highly processed)
- Nutrition Score (France): {nutriments.get('nutrition-score-fr_100g', 'N/A')}
- Carbon Footprint: {nutriments.get('carbon-footprint-from-known-ingredients_product', 'N/A')} g CO₂ (per product)
"""
        return summary.strip()

    except Exception as e:
        return f"⚠️ Error formatting product data: {str(e)}"


# @ProductsRouter.get('/find')
async def getProdInformation(bcode: str = None):
    if bcode:
        response = off_api.product.get(bcode, fields=['nutrient_levels', 'nutriments', 'allergens', 'allergens_from_ingredients', 'categories', 'image_url', 'ingredients_hierarchy', 'ingredients_text_en_ocr_1642445989_result'])
        if response:
            # Save ALL the data to a formatted JSON file
            response = format_product_summary(response)
            print(f"response in json: {response}")
            return response
    else:
        return {"error": "Please provide a name or barcode"}

@ProductsRouter.get('/chat-with-item')
async def chat_with_item(barcode: str, question: str):
    summary = await getProdInformation(barcode)  # from Redis or API
    print(f"summary: {summary}, \n\n\n\nquestion: {question}")
    answer = await query_groq(summary, question)
    return {"answer": answer}