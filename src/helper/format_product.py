def format_product_summary(data: dict) -> dict:
    """
    Returns:
      {
        "display_result": "<markdown string>",   # compact, frontend-ready (render with marked.parse)
        "assistant_context": <raw product_data>   # full product JSON for LLM/context
      }
    """
    try:
        # --- helpers ---
        def first(*keys):
            for k in keys:
                v = data.get(k)
                if v:
                    return v
            return None

        def to_num(x):
            try:
                return float(x)
            except Exception:
                return None

        def format_nutrient(v, unit="g", precision=1):
            n = to_num(v)
            return f"{round(n, precision)} {unit}" if n is not None else "N/A"

        def level_label_sugar(s):
            n = to_num(s)
            if n is None:
                return ""
            if n >= 30:
                return " (Very High)"
            if n >= 15:
                return " (High)"
            if n >= 5:
                return " (Moderate)"
            return " (Low)"

        def dedupe_normalize_allergens(raw):
            if not raw:
                return []
            # raw can be string like "en:milk,en:nuts" or list of tags
            items = []
            if isinstance(raw, str):
                parts = [p.strip() for p in raw.split(",") if p.strip()]
            elif isinstance(raw, (list, tuple)):
                parts = [p.strip() for p in raw if p]
            else:
                parts = []
            seen = []
            for p in parts:
                # remove language prefixes like "en:" and common punctuation
                p2 = p.replace("en:", "").replace("fr:", "").strip()
                p2 = p2.strip().strip("[]()")
                if not p2:
                    continue
                # normalize punctuation and case
                pnorm = p2.lower().replace("_", " ").replace("-", " ").strip()
                # Titlecase for display (keeps localized words)
                pdisplay = pnorm.title()
                if pdisplay not in seen:
                    seen.append(pdisplay)
            return seen

        # --- extract / fallbacks ---
        product_name = first("product_name", "product_name_en", "product_name_fr") or "Product"
        image_url = first("image_url", "image_front_url", "image_front_small_url", "image_small_url") or ""
        category_props = data.get("category_properties", {})
        subtitle = category_props.get("ciqual_food_name:en", None)
        # robust ingredient detection (try several likely fields)
        ingredients = first(
            "ingredients_text",
            "ingredients_text_en",
            "ingredients_text_en_ocr_1642445989_result",
            "ingredients_text_with_allergens"
        ) or "No ingredients listed."

        # allergens: declared tags or allergens field or traces
        declared_allergens = dedupe_normalize_allergens(data.get("allergens_tags") or data.get("allergens"))
        traces = dedupe_normalize_allergens(data.get("traces"))

        # nutriments: pick common keys with fallbacks
        nutriments = data.get("nutriments", {})
        kcal = nutriments.get("energy-kcal_100g") or nutriments.get("energy-kcal") or nutriments.get("energy-kcal_value")
        sugars = nutriments.get("sugars_100g") or nutriments.get("sugars")
        fat = nutriments.get("fat_100g") or nutriments.get("fat")
        sat_fat = nutriments.get("saturated-fat_100g") or nutriments.get("saturated-fat")
        protein = nutriments.get("proteins_100g") or nutriments.get("proteins")
        salt = nutriments.get("salt_100g") or nutriments.get("salt")
        # meta ratings
        nutrition_grade = first("nutrition_grade_fr", "nutrition_grades_tags", "nutrition_grades") or None
        # normalize nutrition_grade when it's a list like ['c']
        if isinstance(nutrition_grade, (list, tuple)) and nutrition_grade:
            nutrition_grade = str(nutrition_grade[0]).upper()
        elif isinstance(nutrition_grade, str):
            nutrition_grade = nutrition_grade.upper()
        else:
            nutrition_grade = "N/A"

        eco_score = first("ecoscore_grade", "ecoscore") or "N/A"

        # --- compute a small health score (same simple rules as before) ---
        score = 100
        recs = []

        s_val = to_num(sugars)
        if s_val is not None and s_val > 15:
            score -= 30
            recs.append("High sugar – limit intake.")
        sat_val = to_num(sat_fat)
        if sat_val is not None and sat_val > 5:
            score -= 20
            recs.append("High saturated fat.")
        nova = to_num(nutriments.get("nova-group") or nutriments.get("nova-group_100g"))
        if nova is not None and int(nova) == 4:
            score -= 15
            recs.append("Ultra-processed food.")
        prot = to_num(protein)
        if prot is not None and prot > 5:
            score += 5
            recs.append("Contains some protein.")
        fv = to_num(nutriments.get("fruits-vegetables-nuts-estimate-from-ingredients_100g"))
        if fv is not None and fv > 5:
            score += 10
            recs.append("Contains fruits/nuts.")

        score = max(0, min(100, int(score)))
        if score >= 70:
            health_label = "Healthy Choice"
        elif score >= 50:
            health_label = "Moderation Recommended"
        else:
            health_label = "Limit Consumption"
        recommendation = " ".join(recs) or "No major concerns."

        # --- Build compact markdown (no categories) ---
        # short ingredients: keep full but strip weird trailing commas/spaces
        ingredients_clean = " ".join(ingredients.replace("\n", " ").split()).strip().rstrip(",")

        # prepare allergen display: declared else traces
        declared_display = ", ".join(declared_allergens) if declared_allergens else "None"
        traces_display = ", ".join(traces) if traces else "None"

        display_md = f"""# {product_name}
{subtitle}

{f'<img src="{image_url}" alt="{product_name}" width="250" height="250" style="border-radius:8px; margin:10px 0;"/>' if image_url else ""}


## ✅ At a Glance
- **Health Rating:** ⚠️ {health_label}  
- **Nutrition Grade:** {nutrition_grade}  
- **Eco-Score:** {eco_score}

<br>

## 🍫 Ingredients
{ingredients_clean}

<br>

## ⚠️ Allergens
- **Contains:** {declared_display}  
- **Traces:** {traces_display}

<br>

## 🍽️ Nutrition Facts (per 100g)
- **Calories:** {format_nutrient(kcal, 'kcal')}  
- **Sugars:** {format_nutrient(sugars)}{level_label_sugar(sugars)}  
- **Fat:** {format_nutrient(fat)} (incl. {format_nutrient(sat_fat)} Sat Fat)  
- **Protein:** {format_nutrient(protein)}  
- **Salt:** {format_nutrient(salt)}

<br>

## **🏆 Health Score :** 
**{score}/100** → {health_label}  
## **💡 Recommendation :** 
{recommendation}
"""

        # assistant_context: keep full raw data so LLM gets everything if needed
        assistant_context = {
            "product_name": product_name,
            "image_url": image_url,
            "ingredients_raw": ingredients,
            "declared_allergens_raw": data.get("allergens"),
            "declared_allergens_tags": data.get("allergens_tags"),
            "traces_raw": data.get("traces"),
            "nutriments": nutriments,
            "raw_product": data
        }

        return {"display_result": display_md.strip(), "assistant_context": assistant_context}

    except Exception as e:
        return {"error": f"⚠️ Error formatting product data: {str(e)}"}
