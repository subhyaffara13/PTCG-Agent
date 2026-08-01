
def expr_type(x: sympy.Basic) -> type:
    import sympy

    if x.kind is sympy.core.kind.BooleanKind:
        return bool
    elif x.is_integer:  # type: ignore[attr-defined]
        return int
    else:
        # NB: Not strictly correct, but we don't support SymPy complex or bool.
        return float

