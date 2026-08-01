
def test_dt_roundlike_tz_options_not_supported(method):
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    with pytest.raises(NotImplementedError, match="ambiguous is not supported."):
        getattr(ser.dt, method)("1h", ambiguous="NaT")

    with pytest.raises(NotImplementedError, match="nonexistent is not supported."):
        getattr(ser.dt, method)("1h", nonexistent="NaT")

