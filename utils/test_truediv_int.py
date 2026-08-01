
def test_truediv_int():
    # This should work, as the result is float:
    assert np.uint8(3) / 123454 == np.float64(3) / 123454

