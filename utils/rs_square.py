
def rs_square(p1, x, prec):
    """
    Square the series modulo ``O(x**prec)``

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_square
    >>> R, x = ring('x', QQ)
    >>> p = x**2 + 2*x + 1
    >>> rs_square(p, x, 3)
    6*x**2 + 4*x + 1
    """
    R = p1.ring
    p = {}
    iv = R.gens.index(x)
    get = p.get
    items = p1.terms()
    items.sort(key=lambda e: e[0][iv])
    monomial_mul = R.monomial_mul
    for i in range(len(items)):
        exp1, v1 = items[i]
        for j in range(i):
            exp2, v2 = items[j]
            if exp1[iv] + exp2[iv] < prec:
                exp = monomial_mul(exp1, exp2)
                p[exp] = get(exp, 0) + v1*v2
            else:
                break
    p = {m: 2*v for m, v in p.items()}
    get = p.get
    for expv, v in p1.iterterms():
        if 2*expv[iv] < prec:
            e2 = monomial_mul(expv, expv)
            p[e2] = get(e2, 0) + v**2
    return R(p)

