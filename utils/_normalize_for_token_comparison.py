
def _normalize_for_token_comparison(value: Any) -> str:
    """Stringify ``value`` for token-rule comparison.

    Booleans are lower-cased so Python's ``True`` / ``False`` line up with
    JSON-style ``"true"`` / ``"false"`` rules from admin config.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)

