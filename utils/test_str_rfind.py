
def test_str_rfind(start, end):
    ser = pd.Series(["abcba", "foo", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.rfind("c", start, end)
    expected = pd.Series([2, -1, None], dtype=ArrowDtype(pa.int64()))
    tm.assert_series_equal(result, expected)

