
def test_put_str_series(temp_hdfstore, performance_warning, string_dtype_arguments):
    # https://github.com/pandas-dev/pandas/pull/60663
    dtype = pd.StringDtype(*string_dtype_arguments)
    ser = Series(["x", pd.NA, "y"], dtype=dtype)

    temp_hdfstore.put("ser", ser)
    expected_dtype = "str" if dtype.na_value is np.nan else "string"
    expected = ser.astype(expected_dtype)
    result = temp_hdfstore.get("ser")
    tm.assert_series_equal(result, expected)

