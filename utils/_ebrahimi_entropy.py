
def _ebrahimi_entropy(X, m, *, xp):
    """Compute the Ebrahimi estimator as described in [6]."""
    # No equation number, but referred to as HE_mn
    n = X.shape[-1]
    X = _pad_along_last_axis(X, m, xp=xp)

    differences = X[..., 2 * m:] - X[..., : -2 * m:]

    i = xp.arange(1, n+1, dtype=X.dtype, device=xp_device(X))
    ci = xp.where(i <= m, 1 + (i - 1)/m, 2.)
    ci = xp.where(i >= n - m + 1, 1 + (n - i)/m, ci)

    logs = xp.log(n * differences / (ci * m))
    return xp.mean(logs, axis=-1)

