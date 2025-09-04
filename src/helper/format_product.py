def format_product_summary(data: dict) -> str:
    try:
        # Helper functions
        def get_nutrient(val, unit='g'):
            return f"{val} {unit}" if val else "None available"
        
        # Extract data
        nutrient_levels = data.get("nutrient_levels", {})
        nutriments = data.get("nutriments", {})
        allergens = data.get("allergens", "None listed").replace("en:", "").split(",")
        allergens_from_ingredients = data.get("allergens_from_ingredients", "").split(",")
        categories = data.get("categories", "").replace(",", " > ")
        image_url = data.get("image_url", "")
        ingredients = data.get("ingredients_text_en_ocr_1642445989_result", "No ingredients listed.")

        # Build the summary
        summary = f"""📦 **Product Categories**:  
{categories}

![Product Image]({image_url})

🍫 **Ingredients**:  
{ingredients.strip()}

⚠️ **Allergens**:  
- **Declared**: {', '.join([a.strip() for a in allergens if a.strip()])}
- **From Ingredients**: {', '.join([a.strip() for a in allergens_from_ingredients if a.strip()])}

🍽️ **Nutrient Levels (per 100g)**:  
""" + "  \n".join([f"- **{k.replace('-', ' ').title()}**: {v.title()}" for k, v in nutrient_levels.items()]) + "  \n\n"

        # Add Nutrition Facts section
        summary += f"""🔬 **Nutrition Facts (per 100g)**:  
- **Calories**: {get_nutrient(nutriments.get('energy-kcal_100g'), 'kcal')}
- **Energy**: {get_nutrient(nutriments.get('energy-kj_100g'), 'kJ')}
- **Carbohydrates**: {get_nutrient(nutriments.get('carbohydrates_100g'))}
- **Sugars**: {get_nutrient(nutriments.get('sugars_100g'))}
- **Fat**: {get_nutrient(nutriments.get('fat_100g'))}
- **Saturated Fat**: {get_nutrient(nutriments.get('saturated-fat_100g'))}
- **Proteins**: {get_nutrient(nutriments.get('proteins_100g'))}
- **Salt**: {get_nutrient(nutriments.get('salt_100g'))}
- **Sodium**: {get_nutrient(nutriments.get('sodium_100g'))}

🌱 **Other Info**:  
- **Fruits/Vegetables/Nuts Estimate**: {nutriments.get('fruits-vegetables-nuts-estimate-from-ingredients_100g', 'None available')}%  
- **NOVA Group**: {nutriments.get('nova-group', 'None available')} (Highly processed)  
- **Nutrition Score (France)**: {nutriments.get('nutrition-score-fr_100g', 'None available')}  
- **Carbon Footprint**: {nutriments.get('carbon-footprint-from-known-ingredients_product', 'None available')} g CO₂ (per product)

"""
        return summary.strip()

    except Exception as e:
        return f"⚠️ Error formatting product data: {str(e)}"
