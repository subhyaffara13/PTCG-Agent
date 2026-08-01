
def test_binary_ufunc_scalar(ufunc, sparse, flip, arrays_for_binary_ufunc):
    # Test that
    #   * ufunc(pd.Series, scalar) == pd.Series(ufunc(array, scalar))
    #   * ufunc(pd.Series, scalar) == ufunc(scalar, pd.Series)
    arr, _ = arrays_for_binary_ufunc
    if sparse:
        arr = SparseArray(arr)
    other = 2
    series = pd.Series(arr, name="name")

    series_args = (series, other)
    array_args = (arr, other)

    if flip:
        series_args = tuple(reversed(series_args))
        array_args = tuple(reversed(array_args))

    expected = pd.Series(ufunc(*array_args), name="name")
    result = ufunc(*series_args)

    tm.assert_series_equal(result, expected)

