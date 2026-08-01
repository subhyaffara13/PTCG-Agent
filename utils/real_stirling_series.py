
def real_stirling_series(x, prec):
    """
    Sums the rational part of Stirling's expansion,

    log(sqrt(2*pi)) - z + 1/(12*z) - 1/(360*z^3) + ...

    """
    t = (MPZ_ONE<<(prec+prec)) // x   # t = 1/x
    u = (t*t)>>prec                  # u = 1/x**2
    s = ln_sqrt2pi_fixed(prec) - x
    # Add initial terms of Stirling's series
    s += t//12;            t = (t*u)>>prec
    s -= t//360;           t = (t*u)>>prec
    s += t//1260;          t = (t*u)>>prec
    s -= t//1680;          t = (t*u)>>prec
    if not t: return s
    s += t//1188;          t = (t*u)>>prec
    s -= 691*t//360360;    t = (t*u)>>prec
    s += t//156;           t = (t*u)>>prec
    if not t: return s
    s -= 3617*t//122400;   t = (t*u)>>prec
    s += 43867*t//244188;  t = (t*u)>>prec
    s -= 174611*t//125400;  t = (t*u)>>prec
    if not t: return s
    k = 22
    # From here on, the coefficients are growing, so we
    # have to keep t at a roughly constant size
    usize = bitcount(abs(u))
    tsize = bitcount(abs(t))
    texp = 0
    while 1:
        p, q, pb, qb = stirling_coefficient(k)
        term_mag = tsize + pb + texp
        shift = -texp
        m = pb - term_mag
        if m > 0 and shift < m:
            p >>= m
            shift -= m
        m = tsize - term_mag
        if m > 0 and shift < m:
            w = t >> m
            shift -= m
        else:
            w = t
        term = (t*p//q) >> shift
        if not term:
            break
        s += term
        t = (t*u) >> usize
        texp -= (prec - usize)
        k += 2
    return s

