
def _default_exception_debug_action(
    instring: str,
    loc: int,
    expr: ParserElement,
    exc: Exception,
    cache_hit: bool = False,
):
    cache_hit_str = "*" if cache_hit else ""
    print(f"{cache_hit_str}Match {expr} failed, {type(exc).__name__} raised: {exc}")


def _defaultExceptionDebugAction(instring, loc, expr, exc):
    print("Exception raised:" + _ustr(exc))

