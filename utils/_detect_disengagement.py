from typing import Optional

def _detect_disengagement(curr_user: Optional[str]) -> bool:
    if not curr_user:
        return False
    return any(p.search(curr_user) for p in _DISENGAGEMENT_PATTERNS)

