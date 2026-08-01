
def test_gh_17146():
    # Check that discrete distributions return PMF of zero at non-integral x.
    # See gh-17146.
    x = np.linspace(0, 1, 11)
    p = 0.8
    pmf = bernoulli(p).pmf(x)
    i = (x % 1 == 0)
    assert_allclose(pmf[-1], p)
    assert_allclose(pmf[0], 1-p)
    assert_equal(pmf[~i], 0)

