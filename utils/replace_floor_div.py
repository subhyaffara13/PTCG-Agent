
def replace_floor_div(expr: sympy.Expr) -> sympy.Expr:
    """
    Replace sympy.floor with FloorDiv.
    """

    def replace(expr: sympy.Expr) -> sympy.Expr:
        expr = sympy.together(expr)

        # Division is represented as a Mul with a Rational factor or a Pow with negative
        # exponent. We convert floor(Mul(...)) to FloorDiv(numerator, denominator) by
        # partitioning factors into the numerator and denominator.
        (numerator, denominator) = (sympy.S.One,) * 2
        for arg in sympy.Mul.make_args(expr):
            if isinstance(arg, sympy.Rational):
                numerator *= arg.numerator
                denominator *= arg.denominator
            elif isinstance(arg, sympy.Pow) and arg.exp.is_negative:
                denominator *= arg.base**-arg.exp
            else:
                numerator *= arg

        return FloorDiv(numerator, denominator)

    return expr.replace(sympy.floor, replace)

