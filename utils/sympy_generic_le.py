
def sympy_generic_le(lower, upper):
    if isinstance(lower, sympy.Expr):
        if not isinstance(upper, sympy.Expr):
            raise AssertionError(
                "upper must be a sympy.Expr when lower is a sympy.Expr"
            )
        # instead of lower <= upper, we do upper >= lower since upper is mostly int_oo
        # and we have better code paths there.
        return upper >= lower
    else:
        # only negative condition is True > False
        if not isinstance(lower, SympyBoolean) or not isinstance(upper, SympyBoolean):
            raise AssertionError((lower, upper))
        return not (lower and not upper)

