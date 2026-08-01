
def test_dt_tz_convert_not_tz_raises():
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    with pytest.raises(TypeError, match="Cannot convert tz-naive timestamps"):
        ser.dt.tz_convert("UTC")

