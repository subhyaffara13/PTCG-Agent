
def test_contains_compiled_regex_flags(any_string_dtype):
    # ensure other (than ignorecase) flags are respected
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    ser = Series(["foobar", "foo\nbar", "Baz"], dtype=any_string_dtype)

    pat = re.compile("^ba")
    result = ser.str.contains(pat)
    expected = Series([False, False, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    pat = re.compile("^ba", flags=re.MULTILINE)
    result = ser.str.contains(pat)
    expected = Series([False, True, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    pat = re.compile("^ba", flags=re.MULTILINE | re.IGNORECASE)
    result = ser.str.contains(pat)
    expected = Series([False, True, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

