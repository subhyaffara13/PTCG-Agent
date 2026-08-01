
def test_str_contains_re2_unicode_escape():
    # GH 63901
    ser = pd.Series(["a", "\u0e01", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.contains(r"[\x{0e00}-\x{0e7f}]")
    expected = pd.Series([False, True, None], dtype=ArrowDtype(pa.bool_()))
    tm.assert_series_equal(result, expected)

