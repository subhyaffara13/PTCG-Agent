
def test_value_counts_na():
    arr = pd.array([True, False, pd.NA], dtype="boolean")
    result = arr.value_counts(dropna=False)
    expected = pd.Series([1, 1, 1], index=arr, dtype="Int64", name="count")
    assert expected.index.dtype == arr.dtype
    tm.assert_series_equal(result, expected)

    result = arr.value_counts(dropna=True)
    expected = pd.Series([1, 1], index=arr[:-1], dtype="Int64", name="count")
    assert expected.index.dtype == arr.dtype
    tm.assert_series_equal(result, expected)


def test_value_counts_na():
    arr = pd.array([0.1, 0.2, 0.1, pd.NA], dtype="Float64")
    result = arr.value_counts(dropna=False)
    idx = pd.Index([0.1, 0.2, pd.NA], dtype=arr.dtype)
    assert idx.dtype == arr.dtype
    expected = pd.Series([2, 1, 1], index=idx, dtype="Int64", name="count")
    tm.assert_series_equal(result, expected)

    result = arr.value_counts(dropna=True)
    expected = pd.Series([2, 1], index=idx[:-1], dtype="Int64", name="count")
    tm.assert_series_equal(result, expected)


def test_value_counts_na():
    arr = pd.array([1, 2, 1, pd.NA], dtype="Int64")
    result = arr.value_counts(dropna=False)
    ex_index = pd.Index([1, 2, pd.NA], dtype="Int64")
    assert ex_index.dtype == "Int64"
    expected = pd.Series([2, 1, 1], index=ex_index, dtype="Int64", name="count")
    tm.assert_series_equal(result, expected)

    result = arr.value_counts(dropna=True)
    expected = pd.Series([2, 1], index=arr[:2], dtype="Int64", name="count")
    assert expected.index.dtype == arr.dtype
    tm.assert_series_equal(result, expected)


def test_value_counts_na(dtype):
    if dtype.na_value is np.nan:
        exp_dtype = "int64"
    elif dtype.storage == "pyarrow":
        exp_dtype = "int64[pyarrow]"
    else:
        exp_dtype = "Int64"
    arr = pd.array(["a", "b", "a", pd.NA], dtype=dtype)
    result = arr.value_counts(dropna=False)
    expected = pd.Series([2, 1, 1], index=arr[[0, 1, 3]], dtype=exp_dtype, name="count")
    tm.assert_series_equal(result, expected)

    result = arr.value_counts(dropna=True)
    expected = pd.Series([2, 1], index=arr[:2], dtype=exp_dtype, name="count")
    tm.assert_series_equal(result, expected)

