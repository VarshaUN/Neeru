import os
from fastapi import FastAPI, Request
from app import bolna

app = FastAPI(title="Neeru")
LEVELS: list[dict] = []   # temporary store; we'll move to SQLite later

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/check-in")
def check_in(phone: str):
    return bolna.place_call(os.environ["BOLNA_AGENT_ID"], phone)

@app.post("/webhook/bolna")
async def webhook(request: Request):
    data = await request.json()
    status = data.get("status")
    if status == "completed":
        print("TRANSCRIPT:", data.get("transcript"))
        print("EXTRACTED:", data.get("extracted_data"))
        LEVELS.append({"id": data.get("id"), "extracted": data.get("extracted_data")})
    return {"received": True}