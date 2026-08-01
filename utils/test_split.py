
def test_split(any_string_dtype, method):
    values = Series(["a_b_c", "c_d_e", np.nan, "f_g_h"], dtype=any_string_dtype)

    result = getattr(values.str, method)("_")
    exp = Series([["a", "b", "c"], ["c", "d", "e"], np.nan, ["f", "g", "h"]])
    exp = _convert_na_value(values, exp)
    tm.assert_series_equal(result, exp)

