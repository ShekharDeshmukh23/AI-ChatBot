from typing import Tuple
from .policy import update_gates, next_hint, try_reveal
from .persona import SYSTEM_PROMPT, intro_line
from .memory import get_session, append_history
from .config import settings

def route_message(session_id: str, user_text: str) -> str:
    # Update gates and append history
    update_gates(session_id, user_text)
    append_history(session_id, "user", user_text)

    t = user_text.strip().lower()

    if t in {"hi", "hello", "hey"}:
        return intro_line()

    # Assemble command
    if "assemble fragments" in t or "reveal" in t:
        ok, msg = try_reveal(session_id, settings.secret_key)
        append_history(session_id, "assistant", msg)
        return msg

    # Otherwise, guide progressively
    hint = next_hint(session_id)
    append_history(session_id, "assistant", hint)
    return hint
