
def test_pct_change_empty():
    # GH 57056
    ser = Series([], dtype="float64")
    expected = ser.copy()
    result = ser.pct_change(periods=0)
    tm.assert_series_equal(expected, result)

