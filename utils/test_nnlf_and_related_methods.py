
def test_nnlf_and_related_methods(dist, params):
    rng = np.random.default_rng(983459824)

    if hasattr(dist, 'pdf'):
        logpxf = dist.logpdf
    else:
        logpxf = dist.logpmf

    x = dist.rvs(*params, size=100, random_state=rng)
    ref = -logpxf(x, *params).sum()
    res1 = dist.nnlf(params, x)
    res2 = dist._penalized_nnlf(params, x)
    assert_allclose(res1, ref)
    assert_allclose(res2, ref)

