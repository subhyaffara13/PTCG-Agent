
def has_free_symbols(itr: Iterable[Any]) -> bool:
    return any(isinstance(x, sympy.Expr) and not x.is_number for x in itr)


def has_free_symbols(val: IterateExprs) -> bool:
    """Faster version of bool(free_symbols(val))"""
    return not all((e.is_number or e.is_Boolean) for e in _iterate_exprs(val))

