
def test_apply_reduce_Series(float_frame):
    float_frame.iloc[::2, float_frame.columns.get_loc("A")] = np.nan
    expected = float_frame.mean(axis=1)
    result = float_frame.apply(np.mean, axis=1)
    tm.assert_series_equal(result, expected)

