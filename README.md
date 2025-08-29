# Product-safety (temporary name)

Product-safety is a food product analysis tool.  
It lets users look up products by **barcode or name**, fetches details from [OpenFoodFacts](https://world.openfoodfacts.org/), and uses an LLM to answer product-related questions like:

- "Is this safe if I have an allergy?"
- "Can I eat this while bodybuilding?"
- "How often can I consume this and stay in shape?"

## Features
- 🔎 Lookup products by barcode or name  
- 📦 Get key nutritional, allergen, and ingredient info  
- 💬 Chat-like interface powered by an LLM for product Q&A  

## Tech Stack
- **Backend:** FastAPI (Python)  
- **DB:** SQLite (easy migration to PostgreSQL)  
- **APIs:** OpenFoodFacts, LLM provider (e.g., OpenAI)  

## Run Locally
```bash
# clone repo
git clone https://github.com/yourusername/product-safety.git
cd product-safety

# create virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run server
uvicorn main:app --reload
