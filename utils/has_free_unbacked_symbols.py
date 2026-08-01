
def has_free_unbacked_symbols(x: IterateExprs) -> bool:
    """Faster version of bool(free_unbacked_symbols(val))"""
    from sympy.core.traversal import iterargs

    for s in _iterate_exprs(x):
        for arg in iterargs(s):
            if arg.is_Symbol and symbol_is_type(
                arg, (SymT.UNBACKED_INT, SymT.UNBACKED_FLOAT)
            ):
                return True
    return False

