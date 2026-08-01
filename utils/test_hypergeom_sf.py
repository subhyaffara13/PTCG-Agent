
def test_hypergeom_sf(k, M, n, N, expected, rtol):
    p = hypergeom.sf(k, M, n, N)
    assert_allclose(p, expected, rtol=rtol)

