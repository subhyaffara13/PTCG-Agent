
def test_bdtrik(y, n, p, k):
    # Reference values for y were computed with mpmath using
    # the _binomial_cdf function from above.
    assert_allclose(sp.bdtrik(y, n, p), k, rtol=1e-11)

