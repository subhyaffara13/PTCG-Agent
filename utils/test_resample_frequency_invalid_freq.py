
def test_resample_frequency_invalid_freq(frame_or_series, freq):
    # GH#9586
    msg = f"Invalid frequency: {freq}"

    obj = frame_or_series(range(5), index=period_range("2020-01-01", periods=5))
    with pytest.raises(ValueError, match=msg):
        obj.resample(freq)

