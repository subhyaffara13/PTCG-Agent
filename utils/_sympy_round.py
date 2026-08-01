
def _sympy_round(
    number: sympy.Basic, ndigits: sympy.Basic | None = None
) -> sympy.Basic:
    from torch.utils._sympy.functions import RoundDecimal, RoundToInt

    if ndigits is None:
        return RoundToInt(number)
    else:
        return RoundDecimal(number, ndigits)

