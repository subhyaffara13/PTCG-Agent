
def check_cont_samples(rng, dist, mv_ex, rtol=1e-7, atol=1e-1):
    rvs = rng.rvs(100000)
    mv = rvs.mean(), rvs.var()
    # test the moments only if the variance is finite
    if np.isfinite(mv_ex[1]):
        assert_allclose(mv, mv_ex, rtol=rtol, atol=atol)
    # Cramer Von Mises test for goodness-of-fit
    rvs = rng.rvs(500)
    dist.cdf = np.vectorize(dist.cdf)
    pval = cramervonmises(rvs, dist.cdf).pvalue
    assert pval > 0.1

