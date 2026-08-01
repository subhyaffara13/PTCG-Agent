
def test_sqeuclidean_dtypes():
    # Assert that sqeuclidean returns the right types of values.
    # Integer types should be converted to floating for stability.
    # Floating point types should be the same as the input.
    x = [1, 2, 3]
    y = [4, 5, 6]

    for dtype in [np.int8, np.int16, np.int32, np.int64]:
        d = wsqeuclidean(np.asarray(x, dtype=dtype), np.asarray(y, dtype=dtype))
        assert_(np.issubdtype(d.dtype, np.floating))

    for dtype in [np.uint8, np.uint16, np.uint32, np.uint64]:
        umax = np.iinfo(dtype).max
        d1 = wsqeuclidean([0], np.asarray([umax], dtype=dtype))
        d2 = wsqeuclidean(np.asarray([umax], dtype=dtype), [0])

        assert_equal(d1, d2)
        assert_equal(d1, np.float64(umax)**2)

    dtypes = [np.float32, np.float64, np.complex64, np.complex128]
    for dtype in ['float16', 'float128']:
        # These aren't present in older numpy versions; float128 may also not
        # be present on all platforms.
        if hasattr(np, dtype):
            dtypes.append(getattr(np, dtype))

    for dtype in dtypes:
        d = wsqeuclidean(np.asarray(x, dtype=dtype), np.asarray(y, dtype=dtype))
        assert_equal(d.dtype, dtype)

