
def _sympy_trunc(a: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import TruncToInt

    return TruncToInt(a)

