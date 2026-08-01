
def test_expanding_sem(frame_or_series):
    # GH: 26476
    obj = frame_or_series([0, 1, 2])
    result = obj.expanding().sem()
    if isinstance(result, DataFrame):
        result = Series(result[0].values)
    expected = Series([np.nan, 0.5, (1 / 3) ** 0.5])
    tm.assert_series_equal(result, expected)

