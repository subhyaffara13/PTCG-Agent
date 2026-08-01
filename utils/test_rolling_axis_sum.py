
def test_rolling_axis_sum():
    # see gh-23372.
    df = DataFrame(np.ones((10, 20)))
    expected = DataFrame({i: [np.nan] * 2 + [3.0] * 8 for i in range(20)})
    result = df.rolling(3).sum()
    tm.assert_frame_equal(result, expected)

