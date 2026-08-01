
def test_ewma_nan_handling_cases(s, adjust, ignore_na, w):
    # GH 7603
    s = Series(s)
    expected = (s.multiply(w).cumsum() / Series(w).cumsum()).ffill()
    result = s.ewm(com=2.0, adjust=adjust, ignore_na=ignore_na).mean()

    tm.assert_series_equal(result, expected)
    if ignore_na is False:
        # check that ignore_na defaults to False
        result = s.ewm(com=2.0, adjust=adjust).mean()
        tm.assert_series_equal(result, expected)

