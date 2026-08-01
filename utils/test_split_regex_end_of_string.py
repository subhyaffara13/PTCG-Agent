
def test_split_regex_end_of_string(any_string_dtype):
    # https://github.com/pandas-dev/pandas/pull/63613
    ser = Series(["baz", "bar", "bars", "bar\n"], dtype=any_string_dtype)

    # with dollar sign
    result = ser.str.split("r$", regex=True)
    expected = Series([["baz"], ["ba", ""], ["bars"], ["ba", "\n"]], dtype=object)
    tm.assert_series_equal(result, expected)

    # with \Z (ensure this is translated to \z for pyarrow)
    result = ser.str.split(r"r\Z", regex=True)
    expected = Series([["baz"], ["ba", ""], ["bars"], ["bar\n"]], dtype=object)
    tm.assert_series_equal(result, expected)

    # ensure finding a literal \Z still works
    ser = Series([r"bar\Z", "bar", r"bar\Zs", "bar\n"], dtype=any_string_dtype)
    result = ser.str.split(r"r\\Z", regex=True)
    expected = Series([["ba", ""], ["bar"], ["ba", "s"], ["bar\n"]], dtype=object)
    tm.assert_series_equal(result, expected)

