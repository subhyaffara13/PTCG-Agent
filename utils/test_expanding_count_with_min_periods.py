
def test_expanding_count_with_min_periods(frame_or_series):
    # GH 26996
    result = frame_or_series(range(5)).expanding(min_periods=3).count()
    expected = frame_or_series([np.nan, np.nan, 3.0, 4.0, 5.0])
    tm.assert_equal(result, expected)

