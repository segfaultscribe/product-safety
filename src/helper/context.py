import json
from src.core.redis_client import redis_client

def save_product_info(session_id: str, barcode: str, role: str, content: str):
    key = f"chat:{session_id}:{barcode}"
    history = redis_client.get(key)
    if history:
        messages = json.loads(history)
    else:
        messages = []

    messages.append({"role": role, "content": content})

    # Save with 30 min TTL
    redis_client.setex(key, 1800, json.dumps(messages))
    return messages


def get_history(session_id: str, barcode: str):
    key = f"chat:{session_id}:{barcode}"
    history = redis_client.get(key)
    return json.loads(history) if history else []