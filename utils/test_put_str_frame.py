
def test_put_str_frame(temp_hdfstore, performance_warning, string_dtype_arguments):
    # https://github.com/pandas-dev/pandas/pull/60663
    dtype = pd.StringDtype(*string_dtype_arguments)
    df = DataFrame({"a": pd.array(["x", pd.NA, "y"], dtype=dtype)})

    temp_hdfstore.put("df", df)
    expected_dtype = "str" if dtype.na_value is np.nan else "string"
    expected = df.astype(expected_dtype)
    result = temp_hdfstore.get("df")
    tm.assert_frame_equal(result, expected)

