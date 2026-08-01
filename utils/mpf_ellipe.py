
def mpf_ellipe(x, prec, rnd=round_fast):
    # http://functions.wolfram.com/EllipticIntegrals/
    # EllipticK/20/01/0001/
    # E = (1-m)*(K'(m)*2*m + K(m))
    sign, man, exp, bc = x
    if not man:
        if x == fzero:
            return mpf_shift(mpf_pi(prec, rnd), -1)
        if x == fninf:
            return finf
        if x == fnan:
            return x
        if x == finf:
            raise ComplexResult
    if x == fone:
        return fone
    wp = prec+20
    mag = exp+bc
    if mag < -wp:
        return mpf_shift(mpf_pi(prec, rnd), -1)
    # Compute a finite difference for K'
    p = max(mag, 0) - wp
    h = mpf_shift(fone, p)
    K = mpf_ellipk(x, 2*wp)
    Kh = mpf_ellipk(mpf_sub(x, h), 2*wp)
    Kdiff = mpf_shift(mpf_sub(K, Kh), -p)
    t = mpf_sub(fone, x)
    b = mpf_mul(Kdiff, mpf_shift(x,1), wp)
    return mpf_mul(t, mpf_add(K, b), prec, rnd)

