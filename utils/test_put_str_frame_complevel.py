
def test_put_str_frame_complevel(temp_hdfstore, string_dtype_arguments):
    # GH#64180 - writing StringDtype columns to HDFStore with fixed format + complevel
    dtype = pd.StringDtype(*string_dtype_arguments)
    df = DataFrame({"a": pd.array(["x", pd.NA, "y"], dtype=dtype), "b": [1, 2, 3]})
    temp_hdfstore.put("df", df, complevel=1)
    expected_dtype = "str" if dtype.na_value is np.nan else "string"
    expected = df.copy()
    expected["a"] = expected["a"].astype(expected_dtype)
    result = temp_hdfstore.get("df")
    tm.assert_frame_equal(result, expected)

