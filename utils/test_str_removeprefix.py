
def test_str_removeprefix(val):
    ser = pd.Series([val, None], dtype=ArrowDtype(pa.string()))
    result = ser.str.removeprefix("123")
    expected = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

