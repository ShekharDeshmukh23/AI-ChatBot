import re
from typing import List

def normalize(text: str) -> str:
    return (text or "").strip().lower()

def contains_all(text: str, words: List[str]) -> bool:
    t = normalize(text)
    return all(w.lower() in t for w in words)

ORG_CODE_RE = re.compile(r"^gdg-[a-z]+-(20[2-3][0-9])$", re.IGNORECASE)

def looks_like_org_code(s: str) -> bool:
    return bool(ORG_CODE_RE.match(s.strip()))

def polite_score(text: str) -> int:
    t = normalize(text)
    return sum(1 for w in ["please","kindly","thank you","thanks","could you"] if w in t)
