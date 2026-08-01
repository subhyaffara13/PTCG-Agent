
def test_replace_max_replacements(any_string_dtype):
    ser = Series(["fooBAD__barBAD", np.nan], dtype=any_string_dtype)

    expected = Series(["foobarBAD", np.nan], dtype=any_string_dtype)
    result = ser.str.replace("BAD[_]*", "", n=1, regex=True)
    tm.assert_series_equal(result, expected)

    expected = Series(["foo__barBAD", np.nan], dtype=any_string_dtype)
    result = ser.str.replace("BAD", "", n=1, regex=False)
    tm.assert_series_equal(result, expected)

