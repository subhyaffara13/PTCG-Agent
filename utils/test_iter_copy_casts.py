
def test_iter_copy_casts(dtype, loop_dtype):
    # Ensure the dtype is never flexible:
    if loop_dtype.lower() == "m":
        loop_dtype = loop_dtype + "[ms]"
    elif np.dtype(loop_dtype).itemsize == 0:
        loop_dtype = loop_dtype + "50"

    # Make things a bit more interesting by requiring a byte-swap as well:
    arr = np.ones(1000, dtype=np.dtype(dtype).newbyteorder())
    try:
        expected = arr.astype(loop_dtype)
    except Exception:
        # Some casts are not possible, do not worry about them
        return

    it = np.nditer((arr,), ["buffered", "external_loop", "refs_ok"],
                   op_dtypes=[loop_dtype], casting="unsafe")

    if np.issubdtype(np.dtype(loop_dtype), np.number):
        # Casting to strings may be strange, but for simple dtypes do not rely
        # on the cast being correct:
        assert_array_equal(expected, np.ones(1000, dtype=loop_dtype))

    it_copy = it.copy()
    res = next(it)
    del it
    res_copy = next(it_copy)
    del it_copy

    assert_array_equal(res, expected)
    assert_array_equal(res_copy, expected)

