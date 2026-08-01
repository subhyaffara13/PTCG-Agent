
def test_extract_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    ser = Series(["aa", "abc", "bb\n"], dtype=any_string_dtype)

    # with dollar sign
    result = ser.str.extract("([ab]+)$")
    expected = Series(["aa", np.nan, "bb"], dtype=any_string_dtype).to_frame()
    tm.assert_frame_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.extract(r"([ab]+)\Z")
    expected = Series(["aa", np.nan, np.nan], dtype=any_string_dtype).to_frame()
    tm.assert_frame_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series([r"aa\Z", "abc", "bb\\Z\n"], dtype=any_string_dtype)
    result = ser.str.extract(r"([ab]+)\\Z")
    expected = Series(["aa", np.nan, "bb"], dtype=any_string_dtype).to_frame()
    tm.assert_frame_equal(result, expected)

