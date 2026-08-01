
def test_rolling_forward_cov_corr(func, expected):
    values1 = np.arange(10).reshape(-1, 1)
    values2 = values1 * 2
    values1[5, 0] = 100
    values = np.concatenate([values1, values2], axis=1)

    indexer = FixedForwardWindowIndexer(window_size=3)
    rolling = DataFrame(values).rolling(window=indexer, min_periods=3)
    # We are interested in checking only pairwise covariance / correlation
    result = getattr(rolling, func)().loc[(slice(None), 1), 0]
    result = result.reset_index(drop=True)
    expected = Series(expected).reset_index(drop=True)
    expected.name = result.name
    tm.assert_equal(result, expected)

