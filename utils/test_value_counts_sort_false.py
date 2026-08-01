
def test_value_counts_sort_false(dtype):
    if dtype.na_value is np.nan:
        exp_dtype = "int64"
    elif dtype.storage == "pyarrow":
        exp_dtype = "int64[pyarrow]"
    else:
        exp_dtype = "Int64"
    ser = pd.Series(["a", "b", "c", "b"], dtype=dtype)
    result = ser.value_counts(sort=False)
    expected = pd.Series([1, 2, 1], index=ser[:3], dtype=exp_dtype, name="count")
    tm.assert_series_equal(result, expected)

