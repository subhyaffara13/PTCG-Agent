
def test_longdouble_complex():
    # Simple test to check longdouble and complex combinations, since these
    # need to go through promotion, which longdouble needs to be careful about.
    x = np.longdouble(1)
    assert x + 1j == 1 + 1j
    assert 1j + x == 1 + 1j

