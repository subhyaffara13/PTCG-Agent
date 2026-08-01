
def test_closed_one_entry(func):
    # GH24718
    ser = Series(data=[2], index=date_range("2000", periods=1))
    result = getattr(ser.rolling("10D", closed="left"), func)()
    tm.assert_series_equal(result, Series([np.nan], index=ser.index))

