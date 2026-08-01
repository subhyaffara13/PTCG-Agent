
def _sympy_sym_float(a: sympy.Basic) -> sympy.Basic:
    from torch.utils._sympy.functions import ToFloat

    # NB: Cannot use a * 1.0 here, because 0 * 1.0 is 0 which incorrectly
    # reports that it is an integer
    return ToFloat(a)

