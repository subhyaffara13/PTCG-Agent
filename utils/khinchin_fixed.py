
def khinchin_fixed(prec):
    wp = int(prec + prec**0.5 + 15)
    s = MPZ_ZERO
    fac = from_int(4)
    t = ONE = MPZ_ONE << wp
    pi = mpf_pi(wp)
    pipow = twopi2 = mpf_shift(mpf_mul(pi, pi, wp), 2)
    n = 1
    while 1:
        zeta2n = mpf_abs(mpf_bernoulli(2*n, wp))
        zeta2n = mpf_mul(zeta2n, pipow, wp)
        zeta2n = mpf_div(zeta2n, fac, wp)
        zeta2n = to_fixed(zeta2n, wp)
        term = (((zeta2n - ONE) * t) // n) >> wp
        if term < 100:
            break
        #if not n % 10:
        #    print n, math.log(int(abs(term)))
        s += term
        t += ONE//(2*n+1) - ONE//(2*n)
        n += 1
        fac = mpf_mul_int(fac, (2*n)*(2*n-1), wp)
        pipow = mpf_mul(pipow, twopi2, wp)
    s = (s << wp) // ln2_fixed(wp)
    K = mpf_exp(from_man_exp(s, -wp), wp)
    K = to_fixed(K, prec)
    return K

