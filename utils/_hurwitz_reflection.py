
def _hurwitz_reflection(ctx, s, a, d, atype):
    # TODO: implement for derivatives
    if d != 0:
        raise NotImplementedError
    res = ctx.re(s)
    negs = -s
    # Integer reflection formula
    if ctx.isnpint(s):
        n = int(res)
        if n <= 0:
            return ctx.bernpoly(1-n, a) / (n-1)
    if not (atype == 'Q' or atype == 'Z'):
        raise NotImplementedError
    t = 1-s
    # We now require a to be standardized
    v = 0
    shift = 0
    b = a
    while ctx.re(b) > 1:
        b -= 1
        v -= b**negs
        shift -= 1
    while ctx.re(b) <= 0:
        v += b**negs
        b += 1
        shift += 1
    # Rational reflection formula
    try:
        p, q = a._mpq_
    except:
        assert a == int(a)
        p = int(a)
        q = 1
    p += shift*q
    assert 1 <= p <= q
    g = ctx.fsum(ctx.cospi(t/2-2*k*b)*ctx._hurwitz(t,(k,q)) \
        for k in range(1,q+1))
    g *= 2*ctx.gamma(t)/(2*ctx.pi*q)**t
    v += g
    return v

