
def symbol_is_type(sym: sympy.Basic, prefix: SymT | Iterable[SymT]) -> bool:
    if not isinstance(sym, sympy.Symbol):
        raise AssertionError("expected sympy.Symbol")
    name_str = sym.name.lower()  # Match capitalized names like XBLOCK, RBLOCK
    if isinstance(prefix, SymT):
        return name_str.startswith(prefix_str[prefix])
    else:
        return name_str.startswith(tuple(prefix_str[p] for p in prefix))

