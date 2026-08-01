
def gamma_fixed_taylor(xmpf, x, wp, prec, rnd, type):
    # Determine nearest multiple of N/2
    #n = int(x >> (wp-1))
    #steps = (n-1)>>1
    nearest_int = ((x >> (wp-1)) + MPZ_ONE) >> 1
    one = MPZ_ONE << wp
    coeffs, cwp = gamma_taylor_coefficients(wp)
    if nearest_int > 0:
        r = one
        for i in xrange(nearest_int-1):
            x -= one
            r = (r*x) >> wp
        x -= one
        p = MPZ_ZERO
        for c in coeffs:
            p = c + ((x*p)>>wp)
        p >>= (cwp-wp)
        if type == 0:
            return from_man_exp((r<<wp)//p, -wp, prec, rnd)
        if type == 2:
            return mpf_shift(from_rational(p, (r<<wp), prec, rnd), wp)
        if type == 3:
            return mpf_log(mpf_abs(from_man_exp((r<<wp)//p, -wp)), prec, rnd)
    else:
        r = one
        for i in xrange(-nearest_int):
            r = (r*x) >> wp
            x += one
        p = MPZ_ZERO
        for c in coeffs:
            p = c + ((x*p)>>wp)
        p >>= (cwp-wp)
        if wp - bitcount(abs(x)) > 10:
            # pass very close to 0, so do floating-point multiply
            g = mpf_add(xmpf, from_int(-nearest_int))  # exact
            r = from_man_exp(p*r,-wp-wp)
            r = mpf_mul(r, g, wp)
            if type == 0:
                return mpf_div(fone, r, prec, rnd)
            if type == 2:
                return mpf_pos(r, prec, rnd)
            if type == 3:
                return mpf_log(mpf_abs(mpf_div(fone, r, wp)), prec, rnd)
        else:
            r = from_man_exp(x*p*r,-3*wp)
            if type == 0: return mpf_div(fone, r, prec, rnd)
            if type == 2: return mpf_pos(r, prec, rnd)
            if type == 3: return mpf_neg(mpf_log(mpf_abs(r), prec, rnd))

