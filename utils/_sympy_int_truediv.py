
def _sympy_int_truediv(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import IntTrueDiv

    return IntTrueDiv(a, b)

