
def _correa_entropy(X, m, *, xp):
    """Compute the Correa estimator as described in [6]."""
    # No equation number, but referred to as HC_mn
    n = X.shape[-1]
    X = _pad_along_last_axis(X, m, xp=xp)

    i = xp.arange(1, n+1, device=xp_device(X))
    dj = xp.arange(-m, m+1, device=xp_device(X))[:, None]
    j = i + dj
    j0 = j + m - 1  # 0-indexed version of j

    Xibar = xp.mean(X[..., j0], axis=-2, keepdims=True)
    difference = X[..., j0] - Xibar
    num = xp.sum(difference*dj, axis=-2)  # dj is d-i
    den = n*xp.sum(difference**2, axis=-2)
    return -xp.mean(xp.log(num/den), axis=-1)

