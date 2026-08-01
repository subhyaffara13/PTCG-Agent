
def test_replace_callable(any_string_dtype):
    # GH 15055
    ser = Series(["fooBAD__barBAD", np.nan], dtype=any_string_dtype)

    # test with callable
    repl = lambda m: m.group(0).swapcase()
    result = ser.str.replace("[a-z][A-Z]{2}", repl, n=2, regex=True)
    expected = Series(["foObaD__baRbaD", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

