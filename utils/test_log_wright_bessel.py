
def test_log_wright_bessel(a, b, x, phi, accuracy):
    """Test for log_wright_bessel, in particular for large x."""
    if np.isnan(accuracy):
        assert np.isnan(log_wright_bessel(a, b, x))
    else:
        assert_allclose(log_wright_bessel(a, b, x), phi, rtol=accuracy)

