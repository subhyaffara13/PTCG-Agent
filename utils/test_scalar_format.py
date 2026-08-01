
def test_scalar_format():
    """Test the str.format method with NumPy scalar types"""
    tests = [('{0}', True, np.bool),
            ('{0}', False, np.bool),
            ('{0:d}', 130, np.uint8),
            ('{0:d}', 50000, np.uint16),
            ('{0:d}', 3000000000, np.uint32),
            ('{0:d}', 15000000000000000000, np.uint64),
            ('{0:d}', -120, np.int8),
            ('{0:d}', -30000, np.int16),
            ('{0:d}', -2000000000, np.int32),
            ('{0:d}', -7000000000000000000, np.int64),
            ('{0:g}', 1.5, np.float16),
            ('{0:g}', 1.5, np.float32),
            ('{0:g}', 1.5, np.float64),
            ('{0:g}', 1.5, np.longdouble),
            ('{0:g}', 1.5 + 0.5j, np.complex64),
            ('{0:g}', 1.5 + 0.5j, np.complex128),
            ('{0:g}', 1.5 + 0.5j, np.clongdouble)]

    for (fmat, val, valtype) in tests:
        try:
            assert_equal(fmat.format(val), fmat.format(valtype(val)),
                    f"failed with val {val}, type {valtype}")
        except ValueError as e:
            assert_(False,
                    f"format raised exception (fmt='{fmat}', {val=}, "
                    f"type={valtype!r}, exc='{e}')")

