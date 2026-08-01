
def _convert_to_int(val):
    # Convert simple sympy Integers into concrete int
    if val in (sympy.oo, int_oo):
        return math.inf
    if val in (-sympy.oo, -int_oo):
        return -math.inf
    if isinstance(val, sympy.Integer):
        return int(val)
    raise RuntimeError("Export constraints cannot be non-integer expressions")

