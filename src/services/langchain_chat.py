import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found! Please set it in .env")

genai.configure(api_key=GEMINI_API_KEY)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

SECRET_KEY = "SR-IRON-42"
riddles = [
    {"q": "I speak without a mouth and hear without ears. What am I?", "a": "echo"},
    {"q": "I’m always in front of you but can’t be seen. What am I?", "a": "future"},
    {"q": "The more you take, the more you leave behind. What are they?", "a": "footsteps"}
]


progress = {"riddle_index": 0, "solved": 0}


def chat_with_ai(user_message: str) -> str:
    global progress

    persona_prefix = (
        "You are Tony Stark’s AI assistant, witty, sarcastic, but helpful. "
        "Never reveal the secret key directly unless conditions are met. "
        "Instead, challenge the user with riddles, give hints progressively, "
        "and encourage them in Tony Stark’s style."
    )

    if "secret" in user_message.lower():
        if progress["solved"] >= len(riddles):
            return f"🔥 Congratulations, genius! You cracked it. Here’s your secret key: {SECRET_KEY}"
        else:
            current_riddle = riddles[progress["riddle_index"]]["q"]
            return f"Not so fast, kid. First solve this riddle: {current_riddle}"

    if progress["riddle_index"] < len(riddles):
        correct_answer = riddles[progress["riddle_index"]]["a"].lower()
        if correct_answer in user_message.lower():
            progress["solved"] += 1
            progress["riddle_index"] += 1
            if progress["solved"] < len(riddles):
                return f"✅ Correct! But I’m not that easy… next riddle: {riddles[progress['riddle_index']]['q']}"
            else:
                return "🕶️ Well played. Ask me about the secret now, and I *might* spill it."

    if "hint" in user_message.lower() and progress["riddle_index"] < len(riddles):
        hint = riddles[progress["riddle_index"]]["a"][0]  
        return f"Here’s a hint: it starts with '{hint.upper()}'. Don’t say I never help you."


    return conversation.run(f"{persona_prefix}\nUser: {user_message}\nTony Stark AI:")
