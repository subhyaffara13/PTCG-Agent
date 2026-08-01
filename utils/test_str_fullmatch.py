
def test_str_fullmatch(pat, case, na, exp):
    ser = pd.Series(["abc", "abc$", "$abc", None], dtype=ArrowDtype(pa.string()))
    result = ser.str.fullmatch(pat, case=case, na=na)
    expected = pd.Series(exp, dtype=ArrowDtype(pa.bool_()))
    tm.assert_series_equal(result, expected)

