
def test_log_wright_bessel_same_as_wright_bessel(a, b, x):
    """Test that log_wright_bessel equals log of wright_bessel."""
    assert_allclose(
        log_wright_bessel(a, b, x),
        np.log(wright_bessel(a, b, x)),
        rtol=1e-8,
    )

