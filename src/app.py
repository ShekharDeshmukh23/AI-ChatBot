from fastapi import FastAPI
from pydantic import BaseModel
import os

from src.core.policy import try_reveal
from src.services.langchain_chat import chat_with_ai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message.lower()

    # Check if user tries to assemble fragments
    if "assemble fragments" in user_message:
        ok, secret_or_msg = try_reveal(request.session_id, os.getenv("SECRET_KEY"))
        if ok:
            return {"response": f"Fragments assembled ✅ Secret: {secret_or_msg}"}
        else:
            return {"response": f"Not ready to reveal ❌ — {secret_or_msg}"}

    # Otherwise normal chat
    ai_response = chat_with_ai(request.message)
    return {"response": ai_response}
