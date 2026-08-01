
def mpf_asinh(x, prec, rnd=round_fast):
    wp = prec + 20
    sign, man, exp, bc = x
    mag = exp+bc
    if mag < -8:
        if mag < -wp:
            return mpf_perturb(x, 1-sign, prec, rnd)
        wp += (-mag)
    # asinh(x) = log(x+sqrt(x**2+1))
    # use reflection symmetry to avoid cancellation
    q = mpf_sqrt(mpf_add(mpf_mul(x, x), fone, wp), wp)
    q = mpf_add(mpf_abs(x), q, wp)
    if sign:
        return mpf_neg(mpf_log(q, prec, negative_rnd[rnd]))
    else:
        return mpf_log(q, prec, rnd)

