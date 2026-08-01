
def mpf_log(x, prec, rnd=round_fast):
    """
    Compute the natural logarithm of the mpf value x. If x is negative,
    ComplexResult is raised.
    """
    sign, man, exp, bc = x
    #------------------------------------------------------------------
    # Handle special values
    if not man:
        if x == fzero: return fninf
        if x == finf: return finf
        if x == fnan: return fnan
    if sign:
        raise ComplexResult("logarithm of a negative number")
    wp = prec + 20
    #------------------------------------------------------------------
    # Handle log(2^n) = log(n)*2.
    # Here we catch the only possible exact value, log(1) = 0
    if man == 1:
        if not exp:
            return fzero
        return from_man_exp(exp*ln2_fixed(wp), -wp, prec, rnd)
    mag = exp+bc
    abs_mag = abs(mag)
    #------------------------------------------------------------------
    # Handle x = 1+eps, where log(x) ~ x. We need to check for
    # cancellation when moving to fixed-point math and compensate
    # by increasing the precision. Note that abs_mag in (0, 1) <=>
    # 0.5 < x < 2 and x != 1
    if abs_mag <= 1:
        # Calculate t = x-1 to measure distance from 1 in bits
        tsign = 1-abs_mag
        if tsign:
            tman = (MPZ_ONE<<bc) - man
        else:
            tman = man - (MPZ_ONE<<(bc-1))
        tbc = bitcount(tman)
        cancellation = bc - tbc
        if cancellation > wp:
            t = normalize(tsign, tman, abs_mag-bc, tbc, tbc, 'n')
            return mpf_perturb(t, tsign, prec, rnd)
        else:
            wp += cancellation
        # TODO: if close enough to 1, we could use Taylor series
        # even in the AGM precision range, since the Taylor series
        # converges rapidly
    #------------------------------------------------------------------
    # Another special case:
    # n*log(2) is a good enough approximation
    if abs_mag > 10000:
        if bitcount(abs_mag) > wp:
            return from_man_exp(exp*ln2_fixed(wp), -wp, prec, rnd)
    #------------------------------------------------------------------
    # General case.
    # Perform argument reduction using log(x) = log(x*2^n) - n*log(2):
    # If we are in the Taylor precision range, choose magnitude 0 or 1.
    # If we are in the AGM precision range, choose magnitude -m for
    # some large m; benchmarking on one machine showed m = prec/20 to be
    # optimal between 1000 and 100,000 digits.
    if wp <= LOG_TAYLOR_PREC:
        m = log_taylor_cached(lshift(man, wp-bc), wp)
        if mag:
            m += mag*ln2_fixed(wp)
    else:
        optimal_mag = -wp//LOG_AGM_MAG_PREC_RATIO
        n = optimal_mag - mag
        x = mpf_shift(x, n)
        wp += (-optimal_mag)
        m = -log_agm(to_fixed(x, wp), wp)
        m -= n*ln2_fixed(wp)
    return from_man_exp(m, -wp, prec, rnd)

