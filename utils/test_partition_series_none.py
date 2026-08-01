
def test_partition_series_none(any_string_dtype, method, exp):
    # https://github.com/pandas-dev/pandas/issues/23558
    # None
    s = Series(["a b c", "c d e", np.nan, "f g h", None], dtype=any_string_dtype)
    result = getattr(s.str, method)(expand=False)
    expected = Series(exp)
    expected = _convert_na_value(s, expected)
    tm.assert_series_equal(result, expected)

