
def test_replace_compiled_regex_callable(any_string_dtype):
    # test with callable
    ser = Series(["fooBAD__barBAD", np.nan], dtype=any_string_dtype)
    repl = lambda m: m.group(0).swapcase()
    pat = re.compile("[a-z][A-Z]{2}")
    result = ser.str.replace(pat, repl, n=2, regex=True)
    expected = Series(["foObaD__baRbaD", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

