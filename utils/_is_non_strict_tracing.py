
def _is_non_strict_tracing() -> bool:
    """
    Indicates whether we are inside a non-strict make_fx-based tracing session.
    """
    return _is_non_strict_tracing_flag

