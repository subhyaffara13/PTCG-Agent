
def test_str_join():
    ser = pd.Series(ArrowExtensionArray(pa.array([list("abc"), list("123"), None])))
    result = ser.str.join("=")
    expected = pd.Series(["a=b=c", "1=2=3", None], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

