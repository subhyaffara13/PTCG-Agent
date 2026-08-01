
def test_asfreq_fill_value(index):
    # test for fill value during resampling, issue 3715

    ser = Series(range(len(index)), index=index, name="a")
    idx_range = date_range if isinstance(index, DatetimeIndex) else timedelta_range

    result = ser.resample("1h").asfreq()
    new_index = idx_range(ser.index[0], ser.index[-1], freq="1h")
    expected = ser.reindex(new_index)
    tm.assert_series_equal(result, expected)

    # Explicit cast to float to avoid implicit cast when setting None
    frame = ser.astype("float").to_frame("value")
    frame.iloc[1] = None
    result = frame.resample("1h").asfreq(fill_value=4.0)
    new_index = idx_range(frame.index[0], frame.index[-1], freq="1h")
    expected = frame.reindex(new_index, fill_value=4.0)
    tm.assert_frame_equal(result, expected)

