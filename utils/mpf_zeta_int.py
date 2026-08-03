import math


def mpf_zeta_int(s, prec, rnd=round_fast):
    """
    Optimized computation of zeta(s) for an integer s.
    """
    wp = prec + 20
    s = int(s)
    if s in zeta_int_cache and zeta_int_cache[s][0] >= wp:
        return mpf_pos(zeta_int_cache[s][1], prec, rnd)
    if s < 2:
        if s == 1:
            raise ValueError("zeta(1) pole")
        if not s:
            return mpf_neg(fhalf)
        return mpf_div(mpf_bernoulli(-s+1, wp), from_int(s-1), prec, rnd)
    # 2^-s term vanishes?
    if s >= wp:
        return mpf_perturb(fone, 0, prec, rnd)
    # 5^-s term vanishes?
    elif s >= wp*0.431:
        t = one = 1 << wp
        t += 1 << (wp - s)
        t += one // (MPZ_THREE ** s)
        t += 1 << max(0, wp - s*2)
        return from_man_exp(t, -wp, prec, rnd)
    else:
        # Fast enough to sum directly?
        # Even better, we use the Euler product (idea stolen from pari)
        m = (float(wp)/(s-1) + 1)
        if m < 30:
            needed_terms = int(2.0**m + 1)
            if needed_terms < int(wp/2.54 + 5) / 10:
                t = fone
                for k in list_primes(needed_terms):
                    #print k, needed_terms
                    powprec = int(wp - s*math.log(k,2))
                    if powprec < 2:
                        break
                    a = mpf_sub(fone, mpf_pow_int(from_int(k), -s, powprec), wp)
                    t = mpf_mul(t, a, wp)
                return mpf_div(fone, t, wp)
    # Use Borwein's algorithm
    n = int(wp/2.54 + 5)
    d = borwein_coefficients(n)
    t = MPZ_ZERO
    s = MPZ(s)
    for k in xrange(n):
        t += (((-1)**k * (d[k] - d[n])) << wp) // (k+1)**s
    t = (t << wp) // (-d[n])
    t = (t << wp) // ((1 << wp) - (1 << (wp+1-s)))
    if (s in zeta_int_cache and zeta_int_cache[s][0] < wp) or (s not in zeta_int_cache):
        zeta_int_cache[s] = (wp, from_man_exp(t, -wp-wp))
    return from_man_exp(t, -wp-wp, prec, rnd)

