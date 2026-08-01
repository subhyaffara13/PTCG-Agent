
def _vasicek_entropy(X, m, *, xp):
    """Compute the Vasicek estimator as described in [6] Eq. 1.3."""
    n = X.shape[-1]
    X = _pad_along_last_axis(X, m, xp=xp)
    differences = X[..., 2 * m:] - X[..., : -2 * m:]
    logs = xp.log(n/(2*m) * differences)
    return xp.mean(logs, axis=-1)

