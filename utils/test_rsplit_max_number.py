
def test_rsplit_max_number(any_string_dtype):
    # setting max number of splits, make sure it's from reverse
    values = Series(["a_b_c", "c_d_e", np.nan, "f_g_h"], dtype=any_string_dtype)
    result = values.str.rsplit("_", n=1)
    exp = Series([["a_b", "c"], ["c_d", "e"], np.nan, ["f_g", "h"]])
    exp = _convert_na_value(values, exp)
    tm.assert_series_equal(result, exp)

