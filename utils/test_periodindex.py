
def test_periodindex(box):
    dt = period_range("2019-12-31", periods=3, freq="D")
    ser = Series(dt)
    idx = box(PeriodIndex(ser))
    expected = idx.copy(deep=True)
    ser.iloc[0] = Period("2020-12-31")
    tm.assert_index_equal(idx, expected)

