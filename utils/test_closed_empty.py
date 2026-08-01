
def test_closed_empty(closed, arithmetic_win_operators):
    # GH 26005
    func_name = arithmetic_win_operators
    ser = Series(data=np.arange(5), index=date_range("2000", periods=5, freq="2D"))
    roll = ser.rolling("1D", closed=closed)

    result = getattr(roll, func_name)()
    expected = Series([np.nan] * 5, index=ser.index)
    tm.assert_series_equal(result, expected)

