
def test_divmod_ufunc():
    # binary in, binary out.
    a = np.array([1, 2, 3])
    expected = np.array([NA, NA, NA], dtype=object)

    result = np.divmod(a, NA)
    assert isinstance(result, tuple)
    for arr in result:
        tm.assert_numpy_array_equal(arr, expected)
        tm.assert_numpy_array_equal(arr, expected)

    result = np.divmod(NA, a)
    for arr in result:
        tm.assert_numpy_array_equal(arr, expected)
        tm.assert_numpy_array_equal(arr, expected)

