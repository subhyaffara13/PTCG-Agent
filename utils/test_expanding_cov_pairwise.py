
def test_expanding_cov_pairwise(frame):
    result = frame.expanding().cov()

    rolling_result = frame.rolling(window=len(frame), min_periods=1).cov()

    tm.assert_frame_equal(result, rolling_result)

