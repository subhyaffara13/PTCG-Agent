
def test_rint_big_int():
    # np.rint bug for large integer values on Windows 32-bit and MKL
    # https://github.com/numpy/numpy/issues/6685
    val = 4607998452777363968
    # This is exactly representable in floating point
    assert_equal(val, int(float(val)))
    # Rint should not change the value
    assert_equal(val, np.rint(val))

