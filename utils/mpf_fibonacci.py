
def mpf_fibonacci(x, prec, rnd=round_fast):
    sign, man, exp, bc = x
    if not man:
        if x == fninf:
            return fnan
        return x
    # F(2^n) ~= 2^(2^n)
    size = abs(exp+bc)
    if exp >= 0:
        # Exact
        if size < 10 or size <= bitcount(prec):
            return from_int(ifib(to_int(x)), prec, rnd)
    # Use the modified Binet formula
    wp = prec + size + 20
    a = mpf_phi(wp)
    b = mpf_add(mpf_shift(a, 1), fnone, wp)
    u = mpf_pow(a, x, wp)
    v = mpf_cos_pi(x, wp)
    v = mpf_div(v, u, wp)
    u = mpf_sub(u, v, wp)
    u = mpf_div(u, b, prec, rnd)
    return u

