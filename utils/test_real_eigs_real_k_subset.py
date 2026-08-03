import itertools

def test_real_eigs_real_k_subset():
    rng = np.random.default_rng(2)

    n = 10
    A = random_array(shape=(n, n), density=0.5, rng=rng)
    A.data *= 2
    A.data -= 1
    A += A.T  # make symmetric to test real eigenvalues

    v0 = np.ones(n)

    whichs = ['LM', 'SM', 'LR', 'SR', 'LI', 'SI']
    dtypes = [np.float32, np.float64]

    for which, sigma, dtype in itertools.product(whichs, [None, 0, 5], dtypes):
        prev_w = np.array([], dtype=dtype)
        eps = np.finfo(dtype).eps
        for k in range(1, 9):
            w, z = eigs(A.astype(dtype), k=k, which=which, sigma=sigma,
                        v0=v0.astype(dtype), tol=0)
            assert_allclose(np.linalg.norm(A.dot(z) - z * w), 0, atol=np.sqrt(eps))

            # Check that the set of eigenvalues for `k` is a subset of that for `k+1`
            dist = abs(prev_w[:,None] - w).min(axis=1)
            assert_allclose(dist, 0, atol=np.sqrt(eps))

            prev_w = w

