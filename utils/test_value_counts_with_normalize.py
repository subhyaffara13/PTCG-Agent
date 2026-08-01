
def test_value_counts_with_normalize():
    ser = pd.Series([True, False, pd.NA], dtype="boolean")
    result = ser.value_counts(normalize=True)
    expected = pd.Series([1, 1], index=ser[:-1], dtype="Float64", name="proportion") / 2
    assert expected.index.dtype == "boolean"
    tm.assert_series_equal(result, expected)


def test_value_counts_with_normalize():
    ser = pd.Series([0.1, 0.2, 0.1, pd.NA], dtype="Float64")
    result = ser.value_counts(normalize=True)
    expected = pd.Series([2, 1], index=ser[:2], dtype="Float64", name="proportion") / 3
    assert expected.index.dtype == ser.dtype
    tm.assert_series_equal(result, expected)


def test_value_counts_with_normalize():
    # GH 33172
    ser = pd.Series([1, 2, 1, pd.NA], dtype="Int64")
    result = ser.value_counts(normalize=True)
    expected = pd.Series([2, 1], index=ser[:2], dtype="Float64", name="proportion") / 3
    assert expected.index.dtype == ser.dtype
    tm.assert_series_equal(result, expected)


def test_value_counts_with_normalize(dtype):
    if dtype.na_value is np.nan:
        exp_dtype = np.float64
    elif dtype.storage == "pyarrow":
        exp_dtype = "double[pyarrow]"
    else:
        exp_dtype = "Float64"
    ser = pd.Series(["a", "b", "a", pd.NA], dtype=dtype)
    result = ser.value_counts(normalize=True)
    expected = pd.Series([2, 1], index=ser[:2], dtype=exp_dtype, name="proportion") / 3
    tm.assert_series_equal(result, expected)

