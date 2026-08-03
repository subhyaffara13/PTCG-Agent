import math


def _van_es_entropy(X, m, *, xp):
    """Compute the van Es estimator as described in [6]."""
    # No equation number, but referred to as HVE_mn.
    # Typo: there should be a log within the summation.
    n = X.shape[-1]
    difference = X[..., m:] - X[..., :-m]
    term1 = 1/(n-m) * xp.sum(xp.log((n+1)/m * difference), axis=-1)
    k = xp.arange(m, n+1, dtype=term1.dtype, device=xp_device(X))
    return term1 + xp.sum(1/k) + math.log(m) - math.log(n+1)

