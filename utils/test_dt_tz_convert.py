
def test_dt_tz_convert(unit):
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp(unit, "US/Pacific")),
    )
    result = ser.dt.tz_convert("US/Eastern")
    expected = pd.Series(
        [ser[0].tz_convert("US/Eastern"), None],
        dtype=ArrowDtype(pa.timestamp(unit, "US/Eastern")),
    )
    tm.assert_series_equal(result, expected)

