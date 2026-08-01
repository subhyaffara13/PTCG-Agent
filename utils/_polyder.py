
def _polyder(p, m, *, xp):
    """Differentiate polynomials represented with coefficients.

    p must be a 1-D or 2-D array.  In the 2-D case, each column gives
    the coefficients of a polynomial; the first row holds the coefficients
    associated with the highest power. m must be a nonnegative integer.
    (numpy.polyder doesn't handle the 2-D case.)
    """

    if m == 0:
        result = p
    else:
        n = p.shape[0]
        if n <= m:
            result = xp.zeros_like(p[:1, ...])
        else:
            dp = xp.asarray(p[:-m, ...], copy=True)
            for k in range(m):
                rng = xp.arange(
                    n - k - 1, m - k - 1, -1, dtype=p.dtype, device=xp_device(p)
                )
                dp *= xp.reshape(rng, (n - m,) + (1,) * (p.ndim - 1))
            result = dp
    return result

