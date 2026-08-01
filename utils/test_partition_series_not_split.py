
def test_partition_series_not_split(any_string_dtype, method, exp):
    # https://github.com/pandas-dev/pandas/issues/23558
    # Not split
    s = Series(["abc", "cde", np.nan, "fgh", None], dtype=any_string_dtype)
    result = getattr(s.str, method)("_", expand=False)
    expected = Series(exp)
    expected = _convert_na_value(s, expected)
    tm.assert_series_equal(result, expected)

