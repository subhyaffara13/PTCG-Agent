
def _safe_literal_eval(s: str) -> t.Any:
    """Safely evaluate an expression

    Returns original string if eval fails.

    Use only where types are ambiguous.
    """
    try:
        return literal_eval(s)
    except (NameError, SyntaxError, ValueError):
        return s

