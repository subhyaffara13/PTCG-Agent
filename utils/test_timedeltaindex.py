
def test_timedeltaindex(cons):
    dt = timedelta_range("1 day", periods=3)
    ser = Series(dt)
    idx = cons(ser)
    expected = idx.copy(deep=True)
    ser.iloc[0] = Timedelta("5 days")
    tm.assert_index_equal(idx, expected)

