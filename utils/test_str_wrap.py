
def test_str_wrap():
    ser = pd.Series(["abcba", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.wrap(3)
    expected = pd.Series(["abc\nba", None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

