
def free_unbacked_symbols(x: IterateExprs) -> OrderedSet[sympy.Symbol]:
    """Like free_symbols, but filtered to only report unbacked symbols"""

    # NB: keep synced with is_unbacked_symint
    return OrderedSet(
        s
        for s in free_symbols(x)
        if symbol_is_type(s, (SymT.UNBACKED_INT, SymT.UNBACKED_FLOAT))
    )

