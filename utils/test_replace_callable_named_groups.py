
def test_replace_callable_named_groups(any_string_dtype):
    # test regex named groups
    ser = Series(["Foo Bar Baz", np.nan], dtype=any_string_dtype)
    pat = r"(?P<first>\w+) (?P<middle>\w+) (?P<last>\w+)"
    repl = lambda m: m.group("middle").swapcase()
    result = ser.str.replace(pat, repl, regex=True)
    expected = Series(["bAR", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

