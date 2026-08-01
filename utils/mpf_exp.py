
def mpf_exp(x, prec, rnd=round_fast):
    sign, man, exp, bc = x
    if man:
        mag = bc + exp
        wp = prec + 14
        if sign:
            man = -man
        # TODO: the best cutoff depends on both x and the precision.
        if prec > 600 and exp >= 0:
            # Need about log2(exp(n)) ~= 1.45*mag extra precision
            e = mpf_e(wp+int(1.45*mag))
            return mpf_pow_int(e, man<<exp, prec, rnd)
        if mag < -wp:
            return mpf_perturb(fone, sign, prec, rnd)
        # |x| >= 2
        if mag > 1:
            # For large arguments: exp(2^mag*(1+eps)) =
            # exp(2^mag)*exp(2^mag*eps) = exp(2^mag)*(1 + 2^mag*eps + ...)
            # so about mag extra bits is required.
            wpmod = wp + mag
            offset = exp + wpmod
            if offset >= 0:
                t = man << offset
            else:
                t = man >> (-offset)
            lg2 = ln2_fixed(wpmod)
            n, t = divmod(t, lg2)
            n = int(n)
            t >>= mag
        else:
            offset = exp + wp
            if offset >= 0:
                t = man << offset
            else:
                t = man >> (-offset)
            n = 0
        man = exp_basecase(t, wp)
        return from_man_exp(man, n-wp, prec, rnd)
    if not exp:
        return fone
    if x == fninf:
        return fzero
    return x

