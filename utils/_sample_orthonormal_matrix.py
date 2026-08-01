
def _sample_orthonormal_matrix(n):
    rng = np.random.default_rng(9086764251)
    M = rng.standard_normal((n, n))
    u, s, v = scipy.linalg.svd(M)
    return u

