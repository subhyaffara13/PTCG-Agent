
def test_hypergeom_cdf(k, M, n, N, expected, rtol):
    p = hypergeom.cdf(k, M, n, N)
    assert_allclose(p, expected, rtol=rtol)

