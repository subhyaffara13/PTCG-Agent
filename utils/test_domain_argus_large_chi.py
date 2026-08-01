
def test_domain_argus_large_chi():
    # for large chi, the Gamma distribution is used and the domain has to be
    # transformed. this is a test to ensure that the transformation works
    chi, lb, ub = 5.5, 0.25, 0.75
    rng = FastGeneratorInversion(stats.argus(chi), domain=(lb, ub))
    rng.random_state = 4574
    r = rng.rvs(size=500)
    assert lb <= r.min() < r.max() <= ub
    # perform goodness of fit test with conditional cdf
    cdf = stats.argus(chi).cdf
    prob = cdf(ub) - cdf(lb)
    assert stats.cramervonmises(r, lambda x: cdf(x) / prob).pvalue > 0.05

