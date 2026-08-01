
def test_split_more_than_one_char(any_string_dtype, method):
    # more than one char
    values = Series(["a__b__c", "c__d__e", np.nan, "f__g__h"], dtype=any_string_dtype)
    result = getattr(values.str, method)("__")
    exp = Series([["a", "b", "c"], ["c", "d", "e"], np.nan, ["f", "g", "h"]])
    exp = _convert_na_value(values, exp)
    tm.assert_series_equal(result, exp)

    result = getattr(values.str, method)("__", expand=False)
    tm.assert_series_equal(result, exp)

