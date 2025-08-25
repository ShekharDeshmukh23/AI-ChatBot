# Optional Anthropic wrapper (not used by default)
from typing import List
import os
from anthropic import Anthropic

class AnthropicClient:
    def __init__(self, model: str = "claude-3-5-sonnet-20240620"):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def chat(self, system: str, messages: List[dict]) -> str:
        content = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            system=system,
            messages=[{"role":"user","content":content}],
            temperature=0.4,
        )
        return msg.content[0].text
