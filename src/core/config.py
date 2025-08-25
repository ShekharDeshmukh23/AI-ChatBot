from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY", "CHANGE_ME")
    bot_name: str = os.getenv("BOT_NAME", "Iris")
    bot_tone: str = os.getenv("BOT_TONE", "helpful, playful, professional")
    org_name: str = os.getenv("ORGANIZATION_NAME", "GDG")

settings = Settings()
