
def _sympy_max(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import Max

    return Max(a, b)

