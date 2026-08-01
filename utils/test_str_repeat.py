
def test_str_repeat():
    ser = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.repeat(2)
    expected = pd.Series(["abcabc", None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

