
def test_rolling_sum_all_nan_window_floating_artifacts():
    # GH#41053
    df = DataFrame([0.002, 0.008, 0.005, np.nan, np.nan, np.nan])
    result = df.rolling(3, min_periods=0).sum()
    expected = DataFrame([0.002, 0.010, 0.015, 0.013, 0.005, 0.0])
    tm.assert_frame_equal(result, expected)

