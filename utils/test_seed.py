
def test_seed():
    assert rand() < 1
    seed(1)
    a = rand()
    b = rand()
    seed(1)
    c = rand()
    d = rand()
    assert a == c
    if not c == d:
        assert a != b
    else:
        assert a == b

    abc = 'abc'
    first = list(abc)
    second = list(abc)
    third = list(abc)

    seed(123)
    shuffle(first)

    seed(123)
    shuffle(second)
    _assumptions_shuffle(third)

    assert first == second == third


def test_seed():
    # Test the seed option of the resample method
    def test_seed_sub(gkde_trail):
        n_sample = 200
        # The results should be different without using seed
        samp1 = gkde_trail.resample(n_sample)
        samp2 = gkde_trail.resample(n_sample)
        assert_raises(
            AssertionError, assert_allclose, samp1, samp2, atol=1e-13
        )
        # Use integer seed
        seed = 831
        samp1 = gkde_trail.resample(n_sample, seed=seed)
        samp2 = gkde_trail.resample(n_sample, seed=seed)
        assert_allclose(samp1, samp2, atol=1e-13)
        # Use RandomState
        rstate1 = np.random.RandomState(seed=138)
        samp1 = gkde_trail.resample(n_sample, seed=rstate1)
        rstate2 = np.random.RandomState(seed=138)
        samp2 = gkde_trail.resample(n_sample, seed=rstate2)
        assert_allclose(samp1, samp2, atol=1e-13)

        # check that np.random.Generator can be used (numpy >= 1.17)
        if hasattr(np.random, 'default_rng'):
            # obtain a np.random.Generator object
            rng = np.random.default_rng(1234)
            gkde_trail.resample(n_sample, seed=rng)

    rng = np.random.default_rng(8765678)
    n_basesample = 500
    wn = rng.random(n_basesample)
    # Test 1D case
    xn_1d = rng.normal(0, 1, n_basesample)

    gkde_1d = stats.gaussian_kde(xn_1d)
    test_seed_sub(gkde_1d)
    gkde_1d_weighted = stats.gaussian_kde(xn_1d, weights=wn)
    test_seed_sub(gkde_1d_weighted)

    # Test 2D case
    mean = np.array([1.0, 3.0])
    covariance = np.array([[1.0, 2.0], [2.0, 6.0]])
    xn_2d = rng.multivariate_normal(mean, covariance, size=n_basesample).T

    gkde_2d = stats.gaussian_kde(xn_2d)
    test_seed_sub(gkde_2d)
    gkde_2d_weighted = stats.gaussian_kde(xn_2d, weights=wn)
    test_seed_sub(gkde_2d_weighted)

