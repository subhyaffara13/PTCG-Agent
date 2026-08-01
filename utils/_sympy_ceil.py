
def _sympy_ceil(a: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import CeilToInt

    return CeilToInt(a)

