
def _kolmogn_p(n, x):
    """Computes the PDF for the two-sided Kolmogorov-Smirnov statistic.

    x must be of type float, n of type integer.
    """
    if np.isnan(n):
        return n  # Keep the same type of nan
    if int(n) != n or n <= 0:
        return np.nan
    if x >= 1.0 or x <= 0:
        return 0
    t = n * x
    if t <= 1.0:
        # Ruben-Gambino: n!/n^n * (2t-1)^n -> 2 n!/n^n * n^2 * (2t-1)^(n-1)
        if t <= 0.5:
            return 0.0
        if n <= 140:
            prd = np.prod(np.arange(1, n) * (1.0 / n) * (2 * t - 1))
        else:
            prd = np.exp(_log_nfactorial_div_n_pow_n(n) + (n-1) * np.log(2 * t - 1))
        return prd * 2 * n**2
    if t >= n - 1:
        # Ruben-Gambino : 1-2(1-x)**n -> 2n*(1-x)**(n-1)
        return 2 * (1.0 - x) ** (n-1) * n
    if x >= 0.5:
        return 2 * scipy.stats.ksone.pdf(x, n)

    # Just take a small delta.
    # Ideally x +/- delta would stay within [i/n, (i+1)/n] for some integer a.
    # as the CDF is a piecewise degree n polynomial.
    # It has knots at 1/n, 2/n, ... (n-1)/n
    # and is not a C-infinity function at the knots
    delta = x / 2.0**16
    delta = min(delta, x - 1.0/n)
    delta = min(delta, 0.5 - x)

    def _kk(_x):
        return kolmogn(n, _x)

    return _derivative(_kk, x, dx=delta, order=5)

