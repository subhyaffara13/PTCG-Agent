
def _setup_random_system(xp, batch_A, batch_b):
    rng = np.random.default_rng(1685363802304750)
    n = 10
    A = rng.random(size=(*batch_A, n, n))
    A = A @ A.mT
    b = rng.random((*batch_b, n))
    x0 = rng.random((*batch_b, n))
    dtype = xpx.default_dtype(xp)
    A, b, x0 = (xp.asarray(arr, dtype=dtype) for arr in [A, b, x0])
    return A, b, x0

