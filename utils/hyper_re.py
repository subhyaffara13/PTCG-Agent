
def hyper_re(DE, r, k):
    """
    Converts a DE into a RE.

    Explanation
    ===========

    Performs the substitution:

    .. math::
        x^l f^j(x) \\to (k + 1 - l)_j . a_{k + j - l}

    Normalises the terms so that lowest order of a term is always r(k).

    Examples
    ========

    >>> from sympy import Function, Derivative
    >>> from sympy.series.formal import hyper_re
    >>> from sympy.abc import x, k
    >>> f, r = Function('f'), Function('r')

    >>> hyper_re(-f(x) + Derivative(f(x)), r, k)
    (k + 1)*r(k + 1) - r(k)
    >>> hyper_re(-x*f(x) + Derivative(f(x), (x, 2)), r, k)
    (k + 2)*(k + 3)*r(k + 3) - r(k)

    See Also
    ========

    sympy.series.formal.exp_re
    """
    RE = S.Zero

    g = DE.atoms(Function).pop()
    x = g.atoms(Symbol).pop()

    mini = None
    for t in Add.make_args(DE.expand()):
        coeff, d = t.as_independent(g)
        c, v = coeff.as_independent(x)
        l = v.as_coeff_exponent(x)[1]
        if isinstance(d, Derivative):
            j = d.derivative_count
        else:
            j = 0
        RE += c * rf(k + 1 - l, j) * r(k + j - l)
        if mini is None or j - l < mini:
            mini = j - l

    RE = RE.subs(k, k - mini)

    m = Wild('m')
    return RE.collect(r(k + m))

