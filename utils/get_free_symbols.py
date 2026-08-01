
def get_free_symbols(x: IterateExprs, unbacked_only: bool) -> OrderedSet[sympy.Symbol]:
    if unbacked_only:
        return free_unbacked_symbols(x)
    else:
        return free_symbols(x)

