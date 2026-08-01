
def test_split_more_regex_split(any_string_dtype):
    # regex split
    values = Series(["a,b_c", "c_d,e", np.nan, "f,g,h"], dtype=any_string_dtype)
    result = values.str.split("[,_]")
    exp = Series([["a", "b", "c"], ["c", "d", "e"], np.nan, ["f", "g", "h"]])
    exp = _convert_na_value(values, exp)
    tm.assert_series_equal(result, exp)

