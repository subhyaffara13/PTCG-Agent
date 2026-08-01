
def _normalize_legal(action_string: str) -> str | None:
    """Normalize an OpenSpiel ``P1(h,0,1)`` string to ``h 0 1``."""
    m = _OPENSPIEL_LEGAL_RE.search(action_string or "")
    if not m:
        return None
    return f"{m.group(1).lower()} {int(m.group(2))} {int(m.group(3))}"

