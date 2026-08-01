
def test_swapcase(any_string_dtype):
    s = Series(["FOO", "BAR", np.nan, "Blah", "blurg"], dtype=any_string_dtype)
    result = s.str.swapcase()
    expected = Series(["foo", "bar", np.nan, "bLAH", "BLURG"], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

