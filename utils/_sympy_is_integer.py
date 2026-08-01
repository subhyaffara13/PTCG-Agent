
def _sympy_is_integer(a: sympy.Basic) -> sympy.Basic:
    import sympy

    from torch.utils._sympy.functions import ToFloat

    return sympy.Eq(ToFloat(sympy.floor(a)), a)

