
def _sympy_min(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import Min

    return Min(a, b)

