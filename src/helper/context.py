import json
from src.core.redis_client import redis_client

def save_product_info(session_id: str, role: str, content: str):
    key = f"chat:{session_id}"
    history = redis_client.get(key)
    if history:
        messages = json.loads(history)
    else:
        messages = []
    messages.append({"role": role, "content": content})
    redis_client.setex(key, 1800, json.dumps(messages)) # 30min TTL

    return messages

def get_history(session_id: str):
    key = f"chat:{session_id}"
    history = redis_client.get(key)
    return json.loads(history) if history else []