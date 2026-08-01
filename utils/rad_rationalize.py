
def rad_rationalize(num, den):
    """
    Rationalize ``num/den`` by removing square roots in the denominator;
    num and den are sum of terms whose squares are positive rationals.

    Examples
    ========

    >>> from sympy import sqrt
    >>> from sympy.simplify.radsimp import rad_rationalize
    >>> rad_rationalize(sqrt(3), 1 + sqrt(2)/3)
    (-sqrt(3) + sqrt(6)/3, -7/9)
    """
    if not den.is_Add:
        return num, den
    g, a, b = split_surds(den)
    a = a*sqrt(g)
    num = _mexpand((a - b)*num)
    den = _mexpand(a**2 - b**2)
    return rad_rationalize(num, den)

