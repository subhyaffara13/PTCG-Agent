
def test_str_pad(side, str_func):
    ser = pd.Series(["a", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.pad(width=3, side=side, fillchar="x")
    expected = pd.Series(
        [getattr("a", str_func)(3, "x"), None], dtype=ArrowDtype(pa.string())
    )
    tm.assert_series_equal(result, expected)

