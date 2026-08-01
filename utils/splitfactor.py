
def splitfactor(p, DE, coefficientD=False, z=None):
    """
    Splitting factorization.

    Explanation
    ===========

    Given a derivation D on k[t] and ``p`` in k[t], return (p_n, p_s) in
    k[t] x k[t] such that p = p_n*p_s, p_s is special, and each square
    factor of p_n is normal.

    Page. 100
    """
    kinv = [1/x for x in DE.T[:DE.level]]
    if z:
        kinv.append(z)

    One = Poly(1, DE.t, domain=p.get_domain())
    Dp = derivation(p, DE, coefficientD=coefficientD)
    # XXX: Is this right?
    if p.is_zero:
        return (p, One)

    if not p.expr.has(DE.t):
        s = p.as_poly(*kinv).gcd(Dp.as_poly(*kinv)).as_poly(DE.t)
        n = p.exquo(s)
        return (n, s)

    if not Dp.is_zero:
        h = p.gcd(Dp).to_field()
        g = p.gcd(p.diff(DE.t)).to_field()
        s = h.exquo(g)

        if s.degree(DE.t) == 0:
            return (p, One)

        q_split = splitfactor(p.exquo(s), DE, coefficientD=coefficientD)

        return (q_split[0], q_split[1]*s)
    else:
        return (p, One)

