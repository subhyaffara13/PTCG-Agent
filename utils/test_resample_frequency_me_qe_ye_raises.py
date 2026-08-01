
def test_resample_frequency_ME_QE_YE_raises(frame_or_series, freq):
    # GH#9586
    msg = f"{freq[1:]} is not supported as period frequency"

    obj = frame_or_series(range(5), index=period_range("2020-01-01", periods=5))
    msg = f"Invalid frequency: {freq}"
    with pytest.raises(ValueError, match=msg):
        obj.resample(freq)

