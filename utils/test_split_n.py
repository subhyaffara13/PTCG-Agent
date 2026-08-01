
def test_split_n(any_string_dtype, method, n):
    s = Series(["a b", pd.NA, "b c"], dtype=any_string_dtype)
    expected = Series([["a", "b"], pd.NA, ["b", "c"]])
    result = getattr(s.str, method)(" ", n=n)
    expected = _convert_na_value(s, expected)
    tm.assert_series_equal(result, expected)

