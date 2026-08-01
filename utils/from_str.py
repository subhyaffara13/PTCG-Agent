
def from_str(x, prec, rnd=round_fast):
    """Create a raw mpf from a decimal literal, rounding in the
    specified direction if the input number cannot be represented
    exactly as a binary floating-point number with the given number of
    bits. The literal syntax accepted is the same as for Python
    floats.

    TODO: the rounding does not work properly for large exponents.
    """
    x = x.lower().strip()
    if x in special_str:
        return special_str[x]

    if '/' in x:
        p, q = x.split('/')
        p, q = p.rstrip('l'), q.rstrip('l')
        return from_rational(int(p), int(q), prec, rnd)

    man, exp = str_to_man_exp(x, base=10)

    # XXX: appropriate cutoffs & track direction
    # note no factors of 5
    if abs(exp) > 400:
        s = from_int(man, prec+10)
        s = mpf_mul(s, mpf_pow_int(ften, exp, prec+10), prec, rnd)
    else:
        if exp >= 0:
            s = from_int(man * 10**exp, prec, rnd)
        else:
            s = from_rational(man, 10**-exp, prec, rnd)
    return s

