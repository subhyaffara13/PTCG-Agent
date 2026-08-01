
def mpf_log_hypot(a, b, prec, rnd):
    """
    Computes log(sqrt(a^2+b^2)) accurately.
    """
    # If either a or b is inf/nan/0, assume it to be a
    if not b[1]:
        a, b = b, a
    # a is inf/nan/0
    if not a[1]:
        # both are inf/nan/0
        if not b[1]:
            if a == b == fzero:
                return fninf
            if fnan in (a, b):
                return fnan
            # at least one term is (+/- inf)^2
            return finf
        # only a is inf/nan/0
        if a == fzero:
            # log(sqrt(0+b^2)) = log(|b|)
            return mpf_log(mpf_abs(b), prec, rnd)
        if a == fnan:
            return fnan
        return finf
    # Exact
    a2 = mpf_mul(a,a)
    b2 = mpf_mul(b,b)
    extra = 20
    # Not exact
    h2 = mpf_add(a2, b2, prec+extra)
    cancelled = mpf_add(h2, fnone, 10)
    mag_cancelled = cancelled[2]+cancelled[3]
    # Just redo the sum exactly if necessary (could be smarter
    # and avoid memory allocation when a or b is precisely 1
    # and the other is tiny...)
    if cancelled == fzero or mag_cancelled < -extra//2:
        h2 = mpf_add(a2, b2, prec+extra-min(a2[2],b2[2]))
    return mpf_shift(mpf_log(h2, prec, rnd), -1)

