
def test_cython_fail_agg():
    dr = bdate_range("1/1/2000", periods=50)
    ts = Series(["A", "B", "C", "D", "E"] * 10, dtype=object, index=dr)

    grouped = ts.groupby(lambda x: x.month)
    summed = grouped.sum()
    expected = grouped.agg(np.sum).astype(object)
    tm.assert_series_equal(summed, expected)

