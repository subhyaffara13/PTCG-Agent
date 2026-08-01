
def mpf_cos_sin(x, prec, rnd=round_fast, which=0, pi=False):
    """
    which:
    0 -- return cos(x), sin(x)
    1 -- return cos(x)
    2 -- return sin(x)
    3 -- return tan(x)

    if pi=True, compute for pi*x
    """
    sign, man, exp, bc = x
    if not man:
        if exp:
            c, s = fnan, fnan
        else:
            c, s = fone, fzero
        if which == 0: return c, s
        if which == 1: return c
        if which == 2: return s
        if which == 3: return s

    mag = bc + exp
    wp = prec + 10

    # Extremely small?
    if mag < 0:
        if mag < -wp:
            if pi:
                x = mpf_mul(x, mpf_pi(wp))
            c = mpf_perturb(fone, 1, prec, rnd)
            s = mpf_perturb(x, 1-sign, prec, rnd)
            if which == 0: return c, s
            if which == 1: return c
            if which == 2: return s
            if which == 3: return mpf_perturb(x, sign, prec, rnd)
    if pi:
        if exp >= -1:
            if exp == -1:
                c = fzero
                s = (fone, fnone)[bool(man & 2) ^ sign]
            elif exp == 0:
                c, s = (fnone, fzero)
            else:
                c, s = (fone, fzero)
            if which == 0: return c, s
            if which == 1: return c
            if which == 2: return s
            if which == 3: return mpf_div(s, c, prec, rnd)
        # Subtract nearest half-integer (= mod by pi/2)
        n = ((man >> (-exp-2)) + 1) >> 1
        man = man - (n << (-exp-1))
        mag2 = bitcount(man) + exp
        wp = prec + 10 - mag2
        offset = exp + wp
        if offset >= 0:
            t = man << offset
        else:
            t = man >> (-offset)
        t = (t*pi_fixed(wp)) >> wp
    else:
        t, n, wp = mod_pi2(man, exp, mag, wp)
    c, s = cos_sin_basecase(t, wp)
    m = n & 3
    if   m == 1: c, s = -s, c
    elif m == 2: c, s = -c, -s
    elif m == 3: c, s = s, -c
    if sign:
        s = -s
    if which == 0:
        c = from_man_exp(c, -wp, prec, rnd)
        s = from_man_exp(s, -wp, prec, rnd)
        return c, s
    if which == 1:
        return from_man_exp(c, -wp, prec, rnd)
    if which == 2:
        return from_man_exp(s, -wp, prec, rnd)
    if which == 3:
        return from_rational(s, c, prec, rnd)

