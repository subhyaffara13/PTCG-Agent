
def test_powm1_return_nan(x, y):
    # Test cases where the expected return value is nan.
    p = powm1(x, y)
    assert np.isnan(p)

