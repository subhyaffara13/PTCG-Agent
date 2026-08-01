
def _check_orth(n, dtype, skip_big=False):
    X = np.ones((n, 2), dtype=float).astype(dtype)

    eps = np.finfo(dtype).eps
    tol = 1000 * eps

    Y = orth(X)
    assert_equal(Y.shape, (n, 1))
    assert_allclose(Y, Y.mean(), atol=tol, rtol=1.4e-7)

    Y = orth(X.T)
    assert_equal(Y.shape, (2, 1))
    assert_allclose(Y, Y.mean(), atol=tol)

    if n > 5 and not skip_big:
        rng = np.random.RandomState(1)
        X = rng.rand(n, 5) @ rng.rand(5, n)
        X = X + 1e-4 * rng.rand(n, 1) @ rng.rand(1, n)
        X = X.astype(dtype)

        Y = orth(X, rcond=1e-3)
        assert_equal(Y.shape, (n, 5))

        Y = orth(X, rcond=1e-6)
        assert_equal(Y.shape, (n, 5 + 1))

