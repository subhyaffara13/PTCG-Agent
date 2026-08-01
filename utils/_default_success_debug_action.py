
def _default_success_debug_action(
    instring: str,
    startloc: int,
    endloc: int,
    expr: ParserElement,
    toks: ParseResults,
    cache_hit: bool = False,
):
    cache_hit_str = "*" if cache_hit else ""
    print(f"{cache_hit_str}Matched {expr} -> {toks.as_list()}")


def _defaultSuccessDebugAction(instring, startloc, endloc, expr, toks):
    print("Matched " + _ustr(expr) + " -> " + str(toks.asList()))

