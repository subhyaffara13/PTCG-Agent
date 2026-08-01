
def test_gh18919_ppf_isf_array_args2(dist):
    # a more general version of the test above. Requires that arguments are broadcasted
    # by the infrastructure.
    rng = np.random.default_rng(34873457824358729823)
    q = rng.random(size=(30, 1, 1, 1))
    n = rng.integers(10, 30, size=(10, 1, 1))
    p = rng.random(size=(4, 1))
    loc = rng.integers(5, size=(3,))

    q[rng.random(size=30) > 0.7] = 0
    q[rng.random(size=30) > 0.7] = 1

    args = (q, n, p) if dist == stats.binom else (q, p, n)

    res = dist.ppf(*args, loc=loc)
    ref = np.vectorize(dist.ppf)(*args) + loc
    np.testing.assert_allclose(res, ref)

    res = dist.isf(*args, loc=loc)
    ref = np.vectorize(dist.isf)(*args) + loc
    np.testing.assert_allclose(res, ref)

