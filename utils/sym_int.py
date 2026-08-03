import math


def sym_int(a):
    r"""SymInt-aware utility for int casting.

    Args:
        a (SymInt, SymFloat, or object): Object to cast
    """
    if overrides.has_torch_function_unary(a):
        return overrides.handle_torch_function(sym_int, (a,), a)
    if isinstance(a, SymInt):
        return a
    elif isinstance(a, SymFloat):
        return math.trunc(a)
    return builtins.int(a)  # type: ignore[operator]

