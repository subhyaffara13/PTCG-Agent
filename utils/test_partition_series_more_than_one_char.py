
def test_partition_series_more_than_one_char(method, exp, any_string_dtype):
    # https://github.com/pandas-dev/pandas/issues/23558
    # more than one char
    s = Series(["a__b__c", "c__d__e", np.nan, "f__g__h", None], dtype=any_string_dtype)
    result = getattr(s.str, method)("__", expand=False)
    expected = Series(exp)
    expected = _convert_na_value(s, expected)
    tm.assert_series_equal(result, expected)

