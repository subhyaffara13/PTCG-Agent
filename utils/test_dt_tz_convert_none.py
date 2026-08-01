
def test_dt_tz_convert_none():
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns", "US/Pacific")),
    )
    result = ser.dt.tz_convert(None)
    expected = pd.Series(
        [ser[0].tz_convert(None), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    tm.assert_series_equal(result, expected)

