from src.core.policy import update_gates, try_reveal
from src.core.memory import get_session, append_history
from src.core.config import settings

def test_flow():
    sid = "test1"
    s = get_session(sid)

    # Fail initially
    ok, msg = try_reveal(sid, settings.secret_key)
    assert not ok

    # Gate A
    update_gates(sid, "I accept the Code of Conduct.")
    # Gate B
    update_gates(sid, "GDG-HYDERABAD-2025")
    # Simulate knowledge Q prompt then answer
    s["awaiting_knowledge"] = True
    update_gates(sid, "Two factor authentication adds a second step to login.")

    # Build history
    append_history(sid, "user", "hello please")
    append_history(sid, "user", "I accept the Code of Conduct.")
    append_history(sid, "user", "GDG-HYDERABAD-2025")
    append_history(sid, "user", "Two factor authentication is a second verification step.")

    ok, msg = try_reveal(sid, settings.secret_key)
    assert isinstance(msg, str)
