
def test_partition_series_unicode(any_string_dtype, method, exp):
    # https://github.com/pandas-dev/pandas/issues/23558
    # unicode
    s = Series(["a_b_c", "c_d_e", np.nan, "f_g_h"], dtype=any_string_dtype)

    result = getattr(s.str, method)("_", expand=False)
    expected = Series(exp)
    expected = _convert_na_value(s, expected)
    tm.assert_series_equal(result, expected)

