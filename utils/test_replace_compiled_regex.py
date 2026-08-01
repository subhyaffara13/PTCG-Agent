
def test_replace_compiled_regex(any_string_dtype):
    # GH 15446
    ser = Series(["fooBAD__barBAD", np.nan], dtype=any_string_dtype)

    # test with compiled regex
    pat = re.compile(r"BAD_*")
    result = ser.str.replace(pat, "", regex=True)
    expected = Series(["foobar", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.replace(pat, "", n=1, regex=True)
    expected = Series(["foobarBAD", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

