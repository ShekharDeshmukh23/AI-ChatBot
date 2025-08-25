import uuid
from .core.statemachine import route_message
from .core.memory import get_session

def main():
    sid = str(uuid.uuid4())[:8]
    print(f"Session: {sid}")
    print("Type 'exit' to quit.\n")
    while True:
        msg = input("You: ").strip()
        if msg.lower() == "exit":
            break
        resp = route_message(sid, msg)
        print("Bot:", resp)

if __name__ == "__main__":
    main()
