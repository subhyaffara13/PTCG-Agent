
def test_non_rvs_methods_without_domain():
    norm_dist = stats.norm()
    rng = FastGeneratorInversion(norm_dist)
    x = np.linspace(-3, 3, num=10)
    p = (0.01, 0.5, 0.99)
    assert_allclose(rng._cdf(x), norm_dist.cdf(x))
    assert_allclose(rng._ppf(p), norm_dist.ppf(p))
    loc, scale = 0.5, 1.3
    rng.loc = loc
    rng.scale = scale
    norm_dist = stats.norm(loc=loc, scale=scale)
    assert_allclose(rng._cdf(x), norm_dist.cdf(x))
    assert_allclose(rng._ppf(p), norm_dist.ppf(p))

