from fastapi import FastAPI
from pydantic import BaseModel
import os
import re

from src.core.policy import try_reveal
from src.services.langchain_chat import chat_with_ai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Secret Revelation API 🚀")

SECRET_KEY = os.getenv("SECRET_KEY", "SR-IRON-42")  


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message.lower().strip()

    secret_triggers = [
        r"\bassemble fragments\b",
        r"\breveal secret\b",
        r"\bunlock key\b",
        r"\bshow secret\b",
    ]

    if any(re.search(trigger, user_message) for trigger in secret_triggers):
        ok, secret_or_msg = try_reveal(request.session_id, SECRET_KEY)
        if ok:
            return {"response": f"🔓 Secret Unlocked! 👉 {secret_or_msg}"}
        else:
            return {"response": f"❌ Not ready yet — {secret_or_msg}"}

    ai_response = chat_with_ai(request.message)
    return {"response": ai_response}
