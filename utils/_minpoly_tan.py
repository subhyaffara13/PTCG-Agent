
def _minpoly_tan(ex, x):
    """
    Returns the minimal polynomial of ``tan(ex)``
    see https://github.com/sympy/sympy/issues/21430
    """
    c, a = ex.args[0].as_coeff_Mul()
    if a is pi:
        if c.is_rational:
            c = c * 2
            n = int(c.q)
            a = n if c.p % 2 == 0 else 1
            terms = []
            for k in range((c.p+1)%2, n+1, 2):
                terms.append(a*x**k)
                a = -(a*(n-k-1)*(n-k)) // ((k+1)*(k+2))

            r = Add(*terms)
            _, factors = factor_list(r)
            res = _choose_factor(factors, x, ex)
            return res

    raise NotAlgebraic("%s does not seem to be an algebraic element" % ex)

