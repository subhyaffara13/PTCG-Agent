
def _detect_satisfaction(curr_user: Optional[str]) -> bool:
    if not curr_user:
        return False
    return any(p.search(curr_user) for p in _SATISFACTION_PATTERNS)

