
def test_str_find(sub, start, end, exp):
    ser = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.find(sub, start=start, end=end)
    expected = pd.Series(exp, dtype=ArrowDtype(pa.int64()))
    tm.assert_series_equal(result, expected)

