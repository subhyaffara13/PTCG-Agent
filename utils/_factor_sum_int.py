
def _factor_sum_int(expr, **kwargs):
    """Return Sum or Integral object with factors that are not
    in the wrt variables removed. In cases where there are additive
    terms in the function of the object that are independent, the
    object will be separated into two objects.

    Examples
    ========

    >>> from sympy import Sum, factor_terms
    >>> from sympy.abc import x, y
    >>> factor_terms(Sum(x + y, (x, 1, 3)))
    y*Sum(1, (x, 1, 3)) + Sum(x, (x, 1, 3))
    >>> factor_terms(Sum(x*y, (x, 1, 3)))
    y*Sum(x, (x, 1, 3))

    Notes
    =====

    If a function in the summand or integrand is replaced
    with a symbol, then this simplification should not be
    done or else an incorrect result will be obtained when
    the symbol is replaced with an expression that depends
    on the variables of summation/integration:

    >>> eq = Sum(y, (x, 1, 3))
    >>> factor_terms(eq).subs(y, x).doit()
    3*x
    >>> eq.subs(y, x).doit()
    6
    """
    result = expr.function
    if result == 0:
        return S.Zero
    limits = expr.limits

    # get the wrt variables
    wrt = {i.args[0] for i in limits}

    # factor out any common terms that are independent of wrt
    f = factor_terms(result, **kwargs)
    i, d = f.as_independent(*wrt)
    if isinstance(f, Add):
        return i * expr.func(1, *limits) + expr.func(d, *limits)
    else:
        return i * expr.func(d, *limits)

