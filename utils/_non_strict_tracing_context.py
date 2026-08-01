
def _non_strict_tracing_context():
    """Context manager that sets the non-strict tracing flag."""
    global _is_non_strict_tracing_flag
    old = _is_non_strict_tracing_flag
    try:
        _is_non_strict_tracing_flag = True
        yield
    finally:
        _is_non_strict_tracing_flag = old

