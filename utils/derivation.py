
def derivation(p, DE, coefficientD=False, basic=False):
    """
    Computes Dp.

    Explanation
    ===========

    Given the derivation D with D = d/dx and p is a polynomial in t over
    K(x), return Dp.

    If coefficientD is True, it computes the derivation kD
    (kappaD), which is defined as kD(sum(ai*Xi**i, (i, 0, n))) ==
    sum(Dai*Xi**i, (i, 1, n)) (Definition 3.2.2, page 80).  X in this case is
    T[-1], so coefficientD computes the derivative just with respect to T[:-1],
    with T[-1] treated as a constant.

    If ``basic=True``, the returns a Basic expression.  Elements of D can still be
    instances of Poly.
    """
    if basic:
        r = 0
    else:
        r = Poly(0, DE.t)

    t = DE.t
    if coefficientD:
        if DE.level <= -len(DE.T):
            # 'base' case, the answer is 0.
            return r
        DE.decrement_level()

    D = DE.D[:len(DE.D) + DE.level + 1]
    T = DE.T[:len(DE.T) + DE.level + 1]

    for d, v in zip(D, T):
        pv = p.as_poly(v)
        if pv is None or basic:
            pv = p.as_expr()

        if basic:
            r += d.as_expr()*pv.diff(v)
        else:
            r += (d.as_expr()*pv.diff(v).as_expr()).as_poly(t)

    if basic:
        r = cancel(r)
    if coefficientD:
        DE.increment_level()

    return r

