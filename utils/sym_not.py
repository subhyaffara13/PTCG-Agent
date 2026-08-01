
def sym_not(a):
    r"""SymInt-aware utility for logical negation.

    Args:
        a (SymBool or bool): Object to negate
    """
    import sympy

    if overrides.has_torch_function_unary(a):
        return overrides.handle_torch_function(sym_not, (a,), a)
    if hasattr(a, "__sym_not__"):
        return a.__sym_not__()
    if isinstance(a, sympy.Basic):
        return ~a  # type: ignore[operator]
    return not a


def sym_not(self: BOOL) -> BOOL:
    """sym_not(SymBool self) -> SymBool"""
    return op.Not(self)

