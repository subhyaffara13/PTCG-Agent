
def test_str_findall(flags):
    ser = pd.Series(["abc", "efg", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.findall("b", flags=flags)
    expected = pd.Series([["b"], [], None], dtype=ArrowDtype(pa.list_(pa.string())))
    tm.assert_series_equal(result, expected)

