import math


def _int_to_sympy_int(val: int | None, default) -> sympy.Expr:
    # Convert concrete int into simple sympy Integers
    if val is None:
        return default
    if val in [-int_oo, int_oo]:
        return val
    if val == math.inf:
        return int_oo
    if val == -math.inf:
        return -int_oo
    return sympy.Integer(val)

