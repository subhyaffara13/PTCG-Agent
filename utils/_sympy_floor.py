
def _sympy_floor(a: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import FloorToInt

    return FloorToInt(a)

