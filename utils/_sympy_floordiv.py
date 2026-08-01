
def _sympy_floordiv(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import FloorDiv

    return FloorDiv(a, b)

