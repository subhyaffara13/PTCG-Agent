
def _binom_exact_conf_int(k, n, confidence_level, alternative, *, xp):
    """
    Compute the estimate and confidence interval for the binomial test.

    Returns proportion, prop_low, prop_high
    """
    init = (xp.zeros_like(k), xp.ones_like(k))
    args = (k, n)
    alpha = ((1 - confidence_level) / 2 if alternative == 'two-sided'
             else 1 - confidence_level)

    # I think using the private methods here is fine, since we will only evaluate with
    # valid `p`, `k`, and `n` (or all NaNs). One exception is when `k=0` and
    # `binom._sf(k-1, n, p)`: evaluates to NaN, but that's not a problem because
    # `plow` has a special case for `k=0` below.
    plow = (xp.zeros_like(k) if alternative == 'less' else
            find_root(lambda p, k, n: _SimpleBinomial(n, p).sf(k-1) - alpha,
                      init, args=args).x)
    phigh = (xp.ones_like(k) if alternative == 'greater' else
             find_root(lambda p, k, n: _SimpleBinomial(n, p).cdf(k) - alpha,
                       init, args=args).x)

    plow = xp.where(k == 0, 0.0, plow)
    phigh = xp.where(k == n, 1.0, phigh)
    return plow, phigh

