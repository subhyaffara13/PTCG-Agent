
def rational_laurent_series(num, den, x, r, m, n):
    r"""
    The function computes the Laurent series coefficients
    of a rational function.

    Parameters
    ==========

    num: A Poly object that is the numerator of `f(x)`.
    den: A Poly object that is the denominator of `f(x)`.
    x: The variable of expansion of the series.
    r: The point of expansion of the series.
    m: Multiplicity of r if r is a pole of `f(x)`. Should
    be zero otherwise.
    n: Order of the term upto which the series is expanded.

    Returns
    =======

    series: A dictionary that has power of the term as key
    and coefficient of that term as value.

    Below is a basic outline of how the Laurent series of a
    rational function `f(x)` about `x_0` is being calculated -

    1. Substitute `x + x_0` in place of `x`. If `x_0`
    is a pole of `f(x)`, multiply the expression by `x^m`
    where `m` is the multiplicity of `x_0`. Denote the
    the resulting expression as g(x). We do this substitution
    so that we can now find the Laurent series of g(x) about
    `x = 0`.

    2. We can then assume that the Laurent series of `g(x)`
    takes the following form -

    .. math:: g(x) = \frac{num(x)}{den(x)} = \sum_{m = 0}^{\infty} a_m x^m

    where `a_m` denotes the Laurent series coefficients.

    3. Multiply the denominator to the RHS of the equation
    and form a recurrence relation for the coefficients `a_m`.
    """
    one = Poly(1, x, extension=True)

    if r == oo:
        # Series at x = oo is equal to first transforming
        # the function from x -> 1/x and finding the
        # series at x = 0
        num, den = inverse_transform_poly(num, den, x)
        r = S(0)

    if r:
        # For an expansion about a non-zero point, a
        # transformation from x -> x + r must be made
        num = num.transform(Poly(x + r, x, extension=True), one)
        den = den.transform(Poly(x + r, x, extension=True), one)

    # Remove the pole from the denominator if the series
    # expansion is about one of the poles
    num, den = (num*x**m).cancel(den, include=True)

    # Equate coefficients for the first terms (base case)
    maxdegree = 1 + max(num.degree(), den.degree())
    syms = symbols(f'a:{maxdegree}', cls=Dummy)
    diff = num - den * Poly(syms[::-1], x)
    coeff_diffs = diff.all_coeffs()[::-1][:maxdegree]
    (coeffs, ) = linsolve(coeff_diffs, syms)

    # Use the recursion relation for the rest
    recursion = den.all_coeffs()[::-1]
    div, rec_rhs = recursion[0], recursion[1:]
    series = list(coeffs)
    while len(series) < n:
        next_coeff = Add(*(c*series[-1-n] for n, c in enumerate(rec_rhs))) / div
        series.append(-next_coeff)
    series = {m - i: val for i, val in enumerate(series)}
    return series

