
def test_rvs_ppf_loc_scale():
    loc, scale = 3.5, 2.3
    dist = stats.norm(loc=loc, scale=scale)
    rng = FastGeneratorInversion(dist, random_state=1234)
    r = rng.rvs(size=1000)
    r_rescaled = (r - loc) / scale
    assert stats.cramervonmises(r_rescaled, "norm").pvalue > 0.01
    q = [0.001, 0.1, 0.5, 0.9, 0.999]
    assert_allclose(rng._ppf(q), rng.ppf(q), atol=1e-10)

