
def test_apply_to_empty_series(index, freq):
    # GH 14313
    ser = Series(index=index)

    if freq == "ME" and isinstance(ser.index, TimedeltaIndex):
        msg = (
            "Resampling on a TimedeltaIndex requires fixed-duration `freq`, "
            "e.g. '24h' or '3D', not <MonthEnd>"
        )
        with pytest.raises(ValueError, match=msg):
            ser.resample(freq)
        return
    elif freq == "ME" and isinstance(ser.index, PeriodIndex):
        # index is PeriodIndex, so convert to corresponding Period freq
        freq = "M"
    result = ser.resample(freq, group_keys=False).apply(lambda x: 1)
    expected = ser.resample(freq).apply("sum")

    tm.assert_series_equal(result, expected, check_dtype=False)

