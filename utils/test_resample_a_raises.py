
def test_resample_A_raises(freq):
    msg = f"Invalid frequency: {freq[1:]}"

    s = Series(range(10), index=date_range("20130101", freq="D", periods=10))
    with pytest.raises(ValueError, match=msg):
        s.resample(freq).mean()

