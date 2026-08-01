
def _sympy_pow_by_natural(a: sympy.Basic, b: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import PowByNatural

    return PowByNatural(a, b)

