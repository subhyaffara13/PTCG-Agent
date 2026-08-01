
def test_pyarrow_ambiguous_group_references(pyarrow_string_dtype, pattern, repl):
    # GH#62653
    ser = Series(["One Two Three", "Foo Bar Baz"], dtype=pyarrow_string_dtype)

    result = ser.str.replace(pattern, repl, regex=True)
    expected = Series(["Two0", "Bar0"], dtype=pyarrow_string_dtype)
    tm.assert_series_equal(result, expected)

