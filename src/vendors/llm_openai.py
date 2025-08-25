# Optional OpenAI wrapper (not used by default)
from typing import List
import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def chat(self, system: str, messages: List[dict]) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role":"system","content":system}] + messages,
            temperature=0.4,
        )
        return resp.choices[0].message.content
