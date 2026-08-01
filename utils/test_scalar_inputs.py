
def test_scalar_inputs(domain, x):
    """ pdf, cdf etc should map scalar values to scalars. check with and
    w/o domain since domain impacts pdf, cdf etc
    Take x inside and outside of domain """
    rng = FastGeneratorInversion(stats.norm(), domain=domain)
    assert np.isscalar(rng._cdf(x))
    assert np.isscalar(rng._ppf(0.5))

