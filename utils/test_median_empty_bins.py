
def test_median_empty_bins(observed):
    df = DataFrame(np.random.default_rng(2).integers(0, 44, 500))

    grps = range(0, 55, 5)
    bins = pd.cut(df[0], grps)

    result = df.groupby(bins, observed=observed).median()
    expected = df.groupby(bins, observed=observed).agg(lambda x: x.median())
    tm.assert_frame_equal(result, expected)

