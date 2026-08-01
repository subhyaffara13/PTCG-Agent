
def _default_start_debug_action(
    instring: str, loc: int, expr: ParserElement, cache_hit: bool = False
):
    cache_hit_str = "*" if cache_hit else ""
    print(
        (
            f"{cache_hit_str}Match {expr} at loc {loc}({lineno(loc, instring)},{col(loc, instring)})\n"
            f"  {line(loc, instring)}\n"
            f"  {'^':>{col(loc, instring)}}"
        )
    )


def _defaultStartDebugAction(instring, loc, expr):
    print(("Match " + _ustr(expr) + " at loc " + _ustr(loc) + "(%d,%d)" % (lineno(loc, instring), col(loc, instring))))

