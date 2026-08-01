
def _sympy_float_pow(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import FloatPow

    return FloatPow(a, b)

