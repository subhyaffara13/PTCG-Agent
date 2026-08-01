
def free_symbol_is_type(e: sympy.Expr, prefix: SymT | Iterable[SymT]) -> bool:
    return any(symbol_is_type(v, prefix) for v in e.free_symbols)

