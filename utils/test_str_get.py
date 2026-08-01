
def test_str_get(i, exp):
    ser = pd.Series(["abc", "de", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.get(i)
    expected = pd.Series(exp, dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

