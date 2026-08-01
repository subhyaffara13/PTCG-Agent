
def check_discr_samples(rng, pv, mv_ex, rtol=1e-3, atol=1e-1):
    rvs = rng.rvs(100000)
    # test if the first few moments match
    mv = rvs.mean(), rvs.var()
    assert_allclose(mv, mv_ex, rtol=rtol, atol=atol)
    # normalize
    pv = pv / pv.sum()
    # chi-squared test for goodness-of-fit
    obs_freqs = np.zeros_like(pv)
    _, freqs = np.unique(rvs, return_counts=True)
    freqs = freqs / freqs.sum()
    obs_freqs[:freqs.size] = freqs
    pval = chisquare(obs_freqs, pv).pvalue
    assert pval > 0.1

