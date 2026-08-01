
def test_resample_M_Q_Y_raises(freq):
    msg = f"Invalid frequency: {freq}"

    s = Series(range(10), index=date_range("20130101", freq="D", periods=10))
    with pytest.raises(ValueError, match=msg):
        s.resample(freq).mean()

