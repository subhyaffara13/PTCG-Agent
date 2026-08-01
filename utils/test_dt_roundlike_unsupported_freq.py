
def test_dt_roundlike_unsupported_freq(method):
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    with pytest.raises(ValueError, match="freq='1B' is not supported"):
        getattr(ser.dt, method)("1B")

    with pytest.raises(ValueError, match="Must specify a valid frequency: None"):
        getattr(ser.dt, method)(None)

