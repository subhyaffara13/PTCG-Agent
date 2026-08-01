
def test_str_slice_replace(start, stop, repl, exp):
    ser = pd.Series(["abcd", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.slice_replace(start, stop, repl)
    expected = pd.Series(exp, dtype=ArrowDtype(pa.string()))
    tm.assert_series_equal(result, expected)

