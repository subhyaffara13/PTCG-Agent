
def _force_inline() -> Iterator[None]:
    """
    A context manager used within the dynamo codebase that forces a function
    and nested function calls to be inlined during dynamo tracing.

    When active, check_verbose() will skip all inline/skip decision logic and
    always return SkipResult(False, ...), meaning functions will be inlined.

    See _make_inlined() in utils.py which uses this to ensure that
    a python function is fully traced to produce the needed variable trackers.
    """
    global _force_inline_flag
    old_val = _force_inline_flag
    try:
        _force_inline_flag = True
        yield
    finally:
        _force_inline_flag = old_val

