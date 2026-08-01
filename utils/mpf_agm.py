
def mpf_agm(a, b, prec, rnd=round_fast):
    """
    Computes the arithmetic-geometric mean agm(a,b) for
    nonnegative mpf values a, b.
    """
    asign, aman, aexp, abc = a
    bsign, bman, bexp, bbc = b
    if asign or bsign:
        raise ComplexResult("agm of a negative number")
    # Handle inf, nan or zero in either operand
    if not (aman and bman):
        if a == fnan or b == fnan:
            return fnan
        if a == finf:
            if b == fzero:
                return fnan
            return finf
        if b == finf:
            if a == fzero:
                return fnan
            return finf
        # agm(0,x) = agm(x,0) = 0
        return fzero
    wp = prec + 20
    amag = aexp+abc
    bmag = bexp+bbc
    mag_delta = amag - bmag
    # Reduce to roughly the same magnitude using floating-point AGM
    abs_mag_delta = abs(mag_delta)
    if abs_mag_delta > 10:
        while abs_mag_delta > 10:
            a, b = mpf_shift(mpf_add(a,b,wp),-1), \
                mpf_sqrt(mpf_mul(a,b,wp),wp)
            abs_mag_delta //= 2
        asign, aman, aexp, abc = a
        bsign, bman, bexp, bbc = b
        amag = aexp+abc
        bmag = bexp+bbc
        mag_delta = amag - bmag
    #print to_float(a), to_float(b)
    # Use agm(a,b) = agm(x*a,x*b)/x to obtain a, b ~= 1
    min_mag = min(amag,bmag)
    max_mag = max(amag,bmag)
    n = 0
    # If too small, we lose precision when going to fixed-point
    if min_mag < -8:
        n = -min_mag
    # If too large, we waste time using fixed-point with large numbers
    elif max_mag > 20:
        n = -max_mag
    if n:
        a = mpf_shift(a, n)
        b = mpf_shift(b, n)
    #print to_float(a), to_float(b)
    af = to_fixed(a, wp)
    bf = to_fixed(b, wp)
    g = agm_fixed(af, bf, wp)
    return from_man_exp(g, -wp-n, prec, rnd)

