
def test_pyarrow_backend_group_replacement(pattern, repl, expected_list):
    ser = Series(["var.one[0]", "var.two[1]", "var.three[2]"]).convert_dtypes(
        dtype_backend="pyarrow"
    )
    result = ser.str.replace(pattern, repl, regex=True)
    expected = Series(expected_list).convert_dtypes(dtype_backend="pyarrow")
    tm.assert_series_equal(result, expected)

