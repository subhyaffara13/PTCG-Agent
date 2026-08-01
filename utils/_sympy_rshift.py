
def _sympy_rshift(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import RShift

    return RShift(a, b)

