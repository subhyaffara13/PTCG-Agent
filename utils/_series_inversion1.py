
def _series_inversion1(p, x, prec):
    """
    Univariate series inversion ``1/p`` modulo ``O(x**prec)``.

    The Newton method is used.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import _series_inversion1
    >>> R, x = ring('x', QQ)
    >>> p = x + 1
    >>> _series_inversion1(p, x, 4)
    -x**3 + x**2 - x + 1
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(_series_inversion1, p, x, prec)
    R = p.ring
    zm = R.zero_monom
    c = p[zm]

    # giant_steps does not seem to work with PythonRational numbers with 1 as
    # denominator. This makes sure such a number is converted to integer.
    if prec == int(prec):
        prec = int(prec)

    if zm not in p:
        raise ValueError("No constant term in series")
    if _has_constant_term(p - c, x):
        raise ValueError("p cannot contain a constant term depending on "
                         "parameters")
    if not R.domain.is_unit(c):
        raise ValueError(f"Constant term {c} must be a unit in {R.domain}")

    one = R(1)
    if R.domain is EX:
        one = 1
    if c != one:
        p1 = R(1)/c
    else:
        p1 = R(1)
    for precx in _giant_steps(prec):
        t = 1 - rs_mul(p1, p, x, precx)
        p1 = p1 + rs_mul(p1, t, x, precx)
    return p1

