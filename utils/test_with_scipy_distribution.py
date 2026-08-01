
def test_with_scipy_distribution():
    # test if the setup works with SciPy's rv_frozen distributions
    dist = stats.norm()
    urng = np.random.default_rng(0)
    rng = NumericalInverseHermite(dist, random_state=urng)
    u = np.linspace(0, 1, num=100)
    check_cont_samples(rng, dist, dist.stats())
    assert_allclose(dist.ppf(u), rng.ppf(u))
    # test if it works with `loc` and `scale`
    dist = stats.norm(loc=10., scale=5.)
    rng = NumericalInverseHermite(dist, random_state=urng)
    check_cont_samples(rng, dist, dist.stats())
    assert_allclose(dist.ppf(u), rng.ppf(u))
    # check for discrete distributions
    dist = stats.binom(10, 0.2)
    rng = DiscreteAliasUrn(dist, random_state=urng)
    domain = dist.support()
    pv = dist.pmf(np.arange(domain[0], domain[1]+1))
    check_discr_samples(rng, pv, dist.stats())

