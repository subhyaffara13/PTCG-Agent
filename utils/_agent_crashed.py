from typing import Any

def _agent_crashed(env: Any, idx: int) -> bool:
    """True if agent ``idx`` ended in a non-DONE/INACTIVE status."""
    status = env.state[idx].status if env.state[idx] else None
    if not status:
        return False
    return str(status).upper() not in {"DONE", "INACTIVE", "ACTIVE"}

