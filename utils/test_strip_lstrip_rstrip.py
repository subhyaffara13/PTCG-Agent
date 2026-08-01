
def test_strip_lstrip_rstrip(any_string_dtype, method, exp):
    ser = Series(["  aa   ", " bb \n", np.nan, "cc  "], dtype=any_string_dtype)

    result = getattr(ser.str, method)()
    expected = Series(exp, dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

