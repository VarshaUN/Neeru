import os
import httpx
from dotenv import load_dotenv

load_dotenv(override=True)
BASE = "https://api.bolna.ai"
HEADERS = {"Authorization": f"Bearer {os.environ['BOLNA_API_KEY']}"}

def wallet():
    return httpx.get(f"{BASE}/user/me", headers=HEADERS).json()

def place_call(agent_id: str, phone: str, user_data: dict | None = None):
    body = {"agent_id": agent_id, "recipient_phone_number": phone}
    if user_data:
        body["user_data"] = user_data
    r = httpx.post(f"{BASE}/call", headers=HEADERS, json=body, timeout=30)
    if r.status_code >= 400:
        return {"bolna_status": r.status_code, "bolna_error": r.text, "sent": body}
    return r.json()