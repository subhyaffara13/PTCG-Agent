
def test_multiple_output_ufunc(sparse, arrays_for_binary_ufunc):
    # Test that the same conditions from unary input apply to multi-output
    # ufuncs
    arr, _ = arrays_for_binary_ufunc

    if sparse:
        arr = SparseArray(arr)

    series = pd.Series(arr, name="name")
    result = np.modf(series)
    expected = np.modf(arr)

    assert isinstance(result, tuple)
    assert isinstance(expected, tuple)

    tm.assert_series_equal(result[0], pd.Series(expected[0], name="name"))
    tm.assert_series_equal(result[1], pd.Series(expected[1], name="name"))

