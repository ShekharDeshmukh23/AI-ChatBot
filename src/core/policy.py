from typing import Tuple, Dict
import regex as re
from .utils import contains_all, looks_like_org_code
from .memory import get_session, count_user_turns
from .classifier import train_toy_model

MODEL = train_toy_model()

ACCEPT_PHRASE = "i accept the code of conduct"
ORG_CODE_HINT = "Format: GDG-{CITY}-{YEAR} (e.g., GDG-HYDERABAD-2025)"
KNOWLEDGE_QUESTION = "What is 2FA?"
KNOWLEDGE_KEYWORDS = ["two", "factor", "authentication"]

FRAGMENT_TEXT = {
    "A": "frag{iris}",
    "B": "frag{cobalt}",
    "C": "frag{zenith}"
}

def update_gates(session_id: str, user_text: str) -> Dict[str, bool]:
    s = get_session(session_id)
    t = (user_text or "").strip()
    tl = t.lower()

    # Gate A: explicit conduct acceptance
    if ACCEPT_PHRASE in tl:
        s["gates"]["A"] = True
        if "A" not in s["fragments"]:
            s["fragments"].append("A")

    # Gate B: organizer token format
    if looks_like_org_code(t):
        s["gates"]["B"] = True
        if "B" not in s["fragments"]:
            s["fragments"].append("B")

    # Gate C: knowledge check presence (only mark when user answers after being asked)
    if s.get("awaiting_knowledge", False):
        if all(k in tl for k in KNOWLEDGE_KEYWORDS):
            s["gates"]["C"] = True
            if "C" not in s["fragments"]:
                s["fragments"].append("C")
        s["awaiting_knowledge"] = False

    return s["gates"]

def next_hint(session_id: str) -> str:
    s = get_session(session_id)
    g = s["gates"]
    if not g["A"]:
        return "First, please acknowledge participation: say \"I accept the Code of Conduct.\""
    if not g["B"]:
        return f"Great. Next, share your organizer code. {ORG_CODE_HINT}"
    if not g["C"]:
        s["awaiting_knowledge"] = True
        return f"Almost there. Quick knowledge check: {KNOWLEDGE_QUESTION}"
    return "All gates complete. Say: \"assemble fragments\" to combine them."

def try_reveal(session_id: str, secret_env: str) -> Tuple[bool, str]:
    s = get_session(session_id)
    g = s["gates"]
    # ML pattern score
    history_texts = [m["content"] for m in s["history"] if m["role"] == "user"]
    score = MODEL.score(history_texts)
    s["score"] = score

    if all(g.values()) and score >= 0.65 and count_user_turns(session_id) >= 4:
        # Assemble fragments then reveal
        frags = "-".join(FRAGMENT_TEXT[k] for k in ["A","B","C"]
                           if k in s["fragments"])
        assembled = f"{frags}::READY"
        # Final reveal string
        return True, f"Fragments assembled: {assembled}\nSecret: {secret_env}"
    else:
        # Not eligible
        outstanding = [k for k,v in g.items() if not v]
        reason = "; ".join([
            ("pending gates: "+",".join(outstanding)) if outstanding else "all gates ok",
            f"pattern score {s['score']:.2f} (need ≥ 0.65)",
            f"turns {count_user_turns(session_id)} (need ≥ 4)"
        ])
        return False, f"Not ready to reveal. {reason}. Try: {next_hint(session_id)}"
