
def test_gh_6536():
    z = loggamma(complex(-3.4, +0.0))
    zbar = loggamma(complex(-3.4, -0.0))
    assert_allclose(z, zbar.conjugate(), rtol=1e-15, atol=0)

