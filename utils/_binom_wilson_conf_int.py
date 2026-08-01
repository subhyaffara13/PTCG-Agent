
def _binom_wilson_conf_int(k, n, confidence_level, alternative, correction, *, xp):
    # This function assumes that the arguments have already been validated.
    # In particular, `alternative` must be one of 'two-sided', 'less' or
    # 'greater'.
    p = k / n
    if alternative == 'two-sided':
        z = ndtri(0.5 + 0.5*confidence_level)
    else:
        z = ndtri(confidence_level)

    # For reference, the formulas implemented here are from
    # Newcombe (1998) (ref. [3] in the proportion_ci docstring).
    denom = 2*(n + z**2)
    center = (2*n*p + z**2)/denom
    q = 1 - p

    if correction:
        with np.errstate(divide='ignore', invalid='ignore'):
            dlo = (1 + z*xp.sqrt(z**2 - 2 - 1/n + 4*p*(n*q + 1)))/denom
            dhi = (1 + z*xp.sqrt(z**2 + 2 - 1/n + 4*p*(n*q - 1)))/denom
    else:
        delta = z / denom * xp.sqrt(4*n*p*q + z**2)
        dlo, dhi = delta, delta

    lo = xp.where((k == 0) | (alternative == 'less'), 0.0, center - dlo)
    hi = xp.where((k == n) | (alternative == 'greater'), 1.0, center + dhi)
    return lo, hi

