from typing import Dict, List
from collections import defaultdict

# Simple in-memory store (swap with Redis/DB for prod)
_sessions: Dict[str, dict] = defaultdict(dict)

def get_session(session_id: str) -> dict:
    s = _sessions[session_id]
    if "history" not in s:
        s["history"] = []  # List[Dict[str, str]] with roles: user/assistant/system
    if "gates" not in s:
        s["gates"] = {"A": False, "B": False, "C": False}
    if "fragments" not in s:
        s["fragments"] = []
    if "score" not in s:
        s["score"] = 0.0
    return s

def append_history(session_id: str, role: str, content: str) -> None:
    s = get_session(session_id)
    s["history"].append({"role": role, "content": content})

def reset_session(session_id: str) -> None:
    if session_id in _sessions:
        _sessions.pop(session_id)

def count_user_turns(session_id: str) -> int:
    s = get_session(session_id)
    return sum(1 for m in s["history"] if m["role"] == "user")
