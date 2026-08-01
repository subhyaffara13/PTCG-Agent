
def test_ewm_with_nat_raises(halflife_with_times):
    # GH#38535
    ser = Series(range(1))
    times = DatetimeIndex(["NaT"])
    with pytest.raises(ValueError, match="Cannot convert NaT values to integer"):
        ser.ewm(com=0.1, halflife=halflife_with_times, times=times)

