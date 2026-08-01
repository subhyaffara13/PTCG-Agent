
def _valid_expr(expr):
    """
    return coefficients of expr if it is a univariate polynomial
    with integer coefficients else raise a ValueError.
    """

    if not expr.is_polynomial():
        raise ValueError("The expression should be a polynomial")
    polynomial = Poly(expr)
    if not polynomial.is_univariate:
        raise ValueError("The expression should be univariate")
    if not polynomial.domain == ZZ:
        raise ValueError("The expression should should have integer coefficients")
    return polynomial.all_coeffs()

