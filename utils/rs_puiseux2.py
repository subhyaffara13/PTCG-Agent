
def rs_puiseux2(f, p, q, x, prec):
    """
    Return the puiseux series for `f(p, q, x, prec)`.

    To be used when function ``f`` is implemented only for regular series.
    """
    index = p.ring.gens.index(x)
    n = 1
    for k in p:
        power = k[index]
        if isinstance(power, Rational):
            num, den = power.as_numer_denom()
            n = n*den // igcd(n, den)
        elif power != int(power):
            den = power.denominator
            n = n*den // igcd(n, den)
    if n != 1:
        p1 = pow_xin(p, index, n)
        r = f(p1, q, x, prec*n)
        n1 = QQ(1, n)
        r = pow_xin(r, index, n1)
    else:
        r = f(p, q, x, prec)
    return r

