
def test_translate_mixed_object():
    # Series with non-string values
    s = Series(["a", "b", "c", 1.2])
    table = str.maketrans("abc", "cde")
    expected = Series(["c", "d", "e", np.nan], dtype=object)
    result = s.str.translate(table)
    tm.assert_series_equal(result, expected)

