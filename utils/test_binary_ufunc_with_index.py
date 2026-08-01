
def test_binary_ufunc_with_index(flip, sparse, ufunc, arrays_for_binary_ufunc):
    # Test that
    #   * func(pd.Series(a), pd.Series(b)) == pd.Series(ufunc(a, b))
    #   * ufunc(Index, pd.Series) dispatches to pd.Series (returns a pd.Series)
    a1, a2 = arrays_for_binary_ufunc
    if sparse:
        a1 = SparseArray(a1, dtype=pd.SparseDtype("int64", 0))
        a2 = SparseArray(a2, dtype=pd.SparseDtype("int64", 0))

    name = "name"  # op(pd.Series, array) preserves the name.
    series = pd.Series(a1, name=name)

    other = pd.Index(a2, name=name).astype("int64")

    array_args = (a1, a2)
    series_args = (series, other)  # ufunc(series, array)

    if flip:
        array_args = reversed(array_args)
        series_args = reversed(series_args)  # ufunc(array, series)

    expected = pd.Series(ufunc(*array_args), name=name)
    result = ufunc(*series_args)
    tm.assert_series_equal(result, expected)

