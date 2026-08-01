
def test_str_replace_empty_pattern():
    # https://github.com/pandas-dev/pandas/issues/64941
    ser = pd.Series(["abcd"], dtype=ArrowDtype(pa.string()))

    result = ser.str.replace("", "")
    expected = pd.Series(["abcd"], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

    result = ser.str.replace("", "X")
    expected = pd.Series(["XaXbXcXdX"], dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

