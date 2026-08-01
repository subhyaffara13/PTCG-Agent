
def test_methods_nunique(test_frame):
    # series only
    g = test_frame.groupby("A")
    r = g.resample("2s")
    result = r.B.nunique()
    expected = g.B.apply(lambda x: x.resample("2s").nunique())
    tm.assert_series_equal(result, expected)

