
def is_same_symbol(a: SymbolNode | None, b: SymbolNode | None) -> bool:
    return (
        a == b
        or (isinstance(a, PlaceholderNode) and isinstance(b, PlaceholderNode))
        or is_same_var_from_getattr(a, b)
    )

