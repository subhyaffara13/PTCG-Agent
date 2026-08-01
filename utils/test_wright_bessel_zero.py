
def test_wright_bessel_zero(a, b):
    """Test at x = 0."""
    assert_equal(wright_bessel(a, b, 0.), rgamma(b))
    assert_allclose(log_wright_bessel(a, b, 0.), -loggamma(b))

