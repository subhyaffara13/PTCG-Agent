
def test_astype_float(dtype, any_float_dtype):
    # Don't compare arrays (37974)
    ser = pd.Series(["1.1", pd.NA, "3.3"], dtype=dtype)
    result = ser.astype(any_float_dtype)
    item = np.nan if isinstance(result.dtype, np.dtype) else pd.NA
    expected = pd.Series([1.1, item, 3.3], dtype=any_float_dtype)
    tm.assert_series_equal(result, expected)

