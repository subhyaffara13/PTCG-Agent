
def _sympy_lshift(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import LShift

    return LShift(a, b)

