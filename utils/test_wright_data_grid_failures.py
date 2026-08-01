
def test_wright_data_grid_failures(a, b, x, phi):
    """Test cases of test_data that do not reach relative accuracy of 1e-11"""
    assert_allclose(wright_bessel(a, b, x), phi, rtol=1e-11)

