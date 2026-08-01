
def _random_covariance(dim, evals, rng, singular=False):
    # Generates random covariance matrix with dimensionality `dim` and
    # eigenvalues `evals` using provided Generator `rng`. Randomly sets
    # some evals to zero if `singular` is True.
    A = rng.random((dim, dim))
    A = A @ A.T
    _, v = np.linalg.eigh(A)
    if singular:
        zero_eigs = rng.normal(size=dim) > 0
        evals[zero_eigs] = 0
    cov = v @ np.diag(evals) @ v.T
    return cov

