
def test_asfreq(frame_or_series, index, freq):
    obj = frame_or_series(range(len(index)), index=index)
    idx_range = date_range if isinstance(index, DatetimeIndex) else timedelta_range

    result = obj.resample(freq).asfreq()
    new_index = idx_range(obj.index[0], obj.index[-1], freq=freq)
    expected = obj.reindex(new_index)
    tm.assert_almost_equal(result, expected)

