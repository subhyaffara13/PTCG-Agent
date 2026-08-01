
def test_split_join_roundtrip(any_string_dtype):
    ser = Series(["a_b_c", "c_d_e", np.nan, "f_g_h"], dtype=any_string_dtype)
    result = ser.str.split("_").str.join("_")
    expected = ser.astype(object)
    tm.assert_series_equal(result, expected)

