
def mpc_square(z, prec, rnd=round_fast):
    # (a+b*I)**2 == a**2 - b**2 + 2*I*a*b
    a, b = z
    p = mpf_mul(a,a)
    q = mpf_mul(b,b)
    r = mpf_mul(a,b, prec, rnd)
    re = mpf_sub(p, q, prec, rnd)
    im = mpf_shift(r, 1)
    return re, im

