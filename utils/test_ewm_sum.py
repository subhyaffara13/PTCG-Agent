
def test_ewm_sum(expected_data, ignore):
    # xref from Numbagg tests
    # https://github.com/numbagg/numbagg/blob/v0.2.1/numbagg/test/test_moving.py#L50
    data = Series([10, 0, np.nan, 10])
    result = data.ewm(alpha=0.5, ignore_na=ignore).sum()
    expected = Series(expected_data)
    tm.assert_series_equal(result, expected)

