
def test_binary_ufunc_with_series(
    flip, shuffle, sparse, ufunc, arrays_for_binary_ufunc
):
    # Test that
    #   * func(pd.Series(a), pd.Series(b)) == pd.Series(ufunc(a, b))
    #   with alignment between the indices
    a1, a2 = arrays_for_binary_ufunc
    if sparse:
        a1 = SparseArray(a1, dtype=pd.SparseDtype("int64", 0))
        a2 = SparseArray(a2, dtype=pd.SparseDtype("int64", 0))

    name = "name"  # op(pd.Series, array) preserves the name.
    series = pd.Series(a1, name=name)
    other = pd.Series(a2, name=name)

    idx = np.random.default_rng(2).permutation(len(a1))

    if shuffle:
        other = other.take(idx)
        if flip:
            index = other.align(series)[0].index
        else:
            index = series.align(other)[0].index
    else:
        index = series.index

    array_args = (a1, a2)
    series_args = (series, other)  # ufunc(series, array)

    if flip:
        array_args = tuple(reversed(array_args))
        series_args = tuple(reversed(series_args))  # ufunc(array, series)

    expected = pd.Series(ufunc(*array_args), index=index, name=name)
    result = ufunc(*series_args)
    tm.assert_series_equal(result, expected)

