
def test_distribution_too_many_args():
    rng = np.random.default_rng(5976604568)
    # Check that a TypeError is raised when too many args are given to a method
    # Regression test for ticket 1815.
    x = np.linspace(0.1, 0.7, num=5)
    assert_raises(TypeError, stats.gamma.pdf, x, 2, 3, loc=1.0)
    assert_raises(TypeError, stats.gamma.pdf, x, 2, 3, 4, loc=1.0)
    assert_raises(TypeError, stats.gamma.pdf, x, 2, 3, 4, 5)
    assert_raises(TypeError, stats.gamma.pdf, x, 2, 3, loc=1.0, scale=0.5)
    assert_raises(TypeError, stats.gamma.rvs, 2., 3, loc=1.0, scale=0.5,
                  random_state=rng)
    assert_raises(TypeError, stats.gamma.cdf, x, 2., 3, loc=1.0, scale=0.5)
    assert_raises(TypeError, stats.gamma.ppf, x, 2., 3, loc=1.0, scale=0.5)
    assert_raises(TypeError, stats.gamma.stats, 2., 3, loc=1.0, scale=0.5)
    assert_raises(TypeError, stats.gamma.entropy, 2., 3, loc=1.0, scale=0.5)
    assert_raises(TypeError, stats.gamma.fit, x, 2., 3, loc=1.0, scale=0.5)

    # These should not give errors
    stats.gamma.pdf(x, 2, 3)  # loc=3
    stats.gamma.pdf(x, 2, 3, 4)  # loc=3, scale=4
    stats.gamma.stats(2., 3)
    stats.gamma.stats(2., 3, 4)
    stats.gamma.stats(2., 3, 4, 'mv')
    stats.gamma.rvs(2., 3, 4, 5, random_state=rng)
    stats.gamma.fit(stats.gamma.rvs(2., size=7, random_state=rng), 2.)

    # Also for a discrete distribution
    stats.geom.pmf(x, 2, loc=3)  # no error, loc=3
    assert_raises(TypeError, stats.geom.pmf, x, 2, 3, 4)
    assert_raises(TypeError, stats.geom.pmf, x, 2, 3, loc=4)

    # And for distributions with 0, 2 and 3 args respectively
    assert_raises(TypeError, stats.expon.pdf, x, 3, loc=1.0)
    assert_raises(TypeError, stats.exponweib.pdf, x, 3, 4, 5, loc=1.0)
    assert_raises(TypeError, stats.exponweib.pdf, x, 3, 4, 5, 0.1, 0.1)
    assert_raises(TypeError, stats.ncf.pdf, x, 3, 4, 5, 6, loc=1.0)
    assert_raises(TypeError, stats.ncf.pdf, x, 3, 4, 5, 6, 1.0, scale=0.5)
    stats.ncf.pdf(x, 3, 4, 5, 6, 1.0)  # 3 args, plus loc/scale

