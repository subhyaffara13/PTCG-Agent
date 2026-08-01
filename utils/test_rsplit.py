
def test_rsplit(any_string_dtype):
    # regex split is not supported by rsplit
    values = Series(["a,b_c", "c_d,e", np.nan, "f,g,h"], dtype=any_string_dtype)
    result = values.str.rsplit("[,_]")
    exp = Series([["a,b_c"], ["c_d,e"], np.nan, ["f,g,h"]])
    exp = _convert_na_value(values, exp)
    tm.assert_series_equal(result, exp)

