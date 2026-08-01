
def _wrap_score_cast_func(score_cast_func):
    """Wrap score_cast_func to handle scientific notation in RESP2 byte strings.

    Redis returns scores as byte strings in RESP2, and large numbers may use
    scientific notation (e.g., b'1.7732526297292595e+18'). Python's int() cannot
    parse scientific notation directly.  Rather than unconditionally routing
    through float() (which would change the input type for every custom
    callable), we try the original function first and only fall back to
    converting through float() on ValueError.
    """
    if score_cast_func is float:
        return score_cast_func

    def _safe_cast(x):
        try:
            return score_cast_func(x)
        except (ValueError, TypeError):
            return score_cast_func(float(x))

    return _safe_cast

