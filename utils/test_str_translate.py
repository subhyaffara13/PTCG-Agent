
def test_str_translate():
    ser = pd.Series(["abcba", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.translate({97: "b"})
    expected = pd.Series(["bbcbb", None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

