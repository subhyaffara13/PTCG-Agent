
def test_resample_unit_second_large_years():
    # GH#57427
    index = DatetimeIndex(
        date_range(start=Timestamp("1950-01-01"), periods=10, freq="1000YS", unit="s")
    )
    ser = Series(1, index=index)
    result = ser.resample("2000YS").sum()
    expected = Series(2, index=index[::2])
    tm.assert_series_equal(result, expected)

