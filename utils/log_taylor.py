
def log_taylor(x, prec, r=0):
    """
    Fixed-point calculation of log(x). It is assumed that x is close
    enough to 1 for the Taylor series to converge quickly. Convergence
    can be improved by specifying r > 0 to compute
    log(x^(1/2^r))*2^r, at the cost of performing r square roots.

    The caller must provide sufficient guard bits.
    """
    for i in xrange(r):
        x = isqrt_fast(x<<prec)
    one = MPZ_ONE << prec
    v = ((x-one)<<prec)//(x+one)
    sign = v < 0
    if sign:
        v = -v
    v2 = (v*v) >> prec
    v4 = (v2*v2) >> prec
    s0 = v
    s1 = v//3
    v = (v*v4) >> prec
    k = 5
    while v:
        s0 += v // k
        k += 2
        s1 += v // k
        v = (v*v4) >> prec
        k += 2
    s1 = (s1*v2) >> prec
    s = (s0+s1) << (1+r)
    if sign:
        return -s
    return s

