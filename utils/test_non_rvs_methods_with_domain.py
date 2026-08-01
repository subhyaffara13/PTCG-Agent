
def test_non_rvs_methods_with_domain():
    # as a first step, compare truncated normal against stats.truncnorm
    rng = FastGeneratorInversion(stats.norm(), domain=(2.3, 3.2))
    trunc_norm = stats.truncnorm(2.3, 3.2)
    # take values that are inside and outside the domain
    x = (2.0, 2.4, 3.0, 3.4)
    p = (0.01, 0.5, 0.99)
    assert_allclose(rng._cdf(x), trunc_norm.cdf(x))
    assert_allclose(rng._ppf(p), trunc_norm.ppf(p))
    loc, scale = 2, 3
    rng.loc = 2
    rng.scale = 3
    trunc_norm = stats.truncnorm(2.3, 3.2, loc=loc, scale=scale)
    x = np.array(x) * scale + loc
    assert_allclose(rng._cdf(x), trunc_norm.cdf(x))
    assert_allclose(rng._ppf(p), trunc_norm.ppf(p))

    # do another sanity check with beta distribution
    # in that case, it is important to use the correct domain since beta
    # is a transformation of betaprime which has a different support
    rng = FastGeneratorInversion(stats.beta(2.5, 3.5), domain=(0.3, 0.7))
    rng.loc = 2
    rng.scale = 2.5
    # the support is 2.75, , 3.75 (2 + 2.5 * 0.3, 2 + 2.5 * 0.7)
    assert_array_equal(rng.support(), (2.75, 3.75))
    x = np.array([2.74, 2.76, 3.74, 3.76])
    # the cdf needs to be zero outside of the domain
    y_cdf = rng._cdf(x)
    assert_array_equal((y_cdf[0], y_cdf[3]), (0, 1))
    assert np.min(y_cdf[1:3]) > 0
    # ppf needs to map 0 and 1 to the boundaries
    assert_allclose(rng._ppf(y_cdf), (2.75, 2.76, 3.74, 3.75))

