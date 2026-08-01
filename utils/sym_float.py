
def sym_float(a):
    r"""SymInt-aware utility for float casting.

    Args:
        a (SymInt, SymFloat, or object): Object to cast
    """
    if overrides.has_torch_function_unary(a):
        return overrides.handle_torch_function(sym_float, (a,), a)
    if isinstance(a, SymFloat):
        return a
    elif hasattr(a, "__sym_float__"):
        return a.__sym_float__()
    return builtins.float(a)  # type: ignore[operator]


def sym_float(self: TensorType) -> FLOAT:
    """sym_float(SymInt self) -> SymFloat"""
    return op.Cast(self, to=FLOAT.dtype)

