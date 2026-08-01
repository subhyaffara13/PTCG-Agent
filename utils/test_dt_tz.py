
def test_dt_tz(tz):
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns", tz=tz)),
    )
    result = ser.dt.tz
    assert result == timezones.maybe_get_tz(tz)

