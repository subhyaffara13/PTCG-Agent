
def check_rvs_broadcast(distfunc, distname, allargs, shape, shape_only, otype):
    rng = np.random.RandomState(123)
    sample = distfunc.rvs(*allargs, random_state=rng)
    assert_equal(sample.shape, shape, f"{distname}: rvs failed to broadcast")
    if not shape_only:
        rvs = np.vectorize(
            lambda *allargs: distfunc.rvs(*allargs, random_state=rng),
            otypes=otype)
        rng = np.random.RandomState(123)
        expected = rvs(*allargs)
        assert_allclose(sample, expected, rtol=1e-13)

