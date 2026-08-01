
def test_str_start_ends_with(side, pat, na, exp):
    ser = pd.Series(["abc", None, "efg"], dtype=ArrowDtype(pa.string()))
    result = getattr(ser.str, side)(pat, na=na)
    expected = pd.Series(exp, dtype=ArrowDtype(pa.bool_()))
    tm.assert_series_equal(result, expected)

