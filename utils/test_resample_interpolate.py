
def test_resample_interpolate(index):
    # GH#12925
    df = DataFrame(range(len(index)), index=index)
    result = df.resample("1min").asfreq().interpolate()
    expected = df.resample("1min").interpolate()
    tm.assert_frame_equal(result, expected)

