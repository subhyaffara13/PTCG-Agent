
def _sympy_float_truediv(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import FloatTrueDiv

    return FloatTrueDiv(a, b)

