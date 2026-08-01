
def test_title(any_string_dtype):
    s = Series(["FOO", "BAR", np.nan, "Blah", "blurg"], dtype=any_string_dtype)
    result = s.str.title()
    expected = Series(["Foo", "Bar", np.nan, "Blah", "Blurg"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

