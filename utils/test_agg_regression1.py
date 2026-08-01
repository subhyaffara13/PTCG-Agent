
def test_agg_regression1(tsframe):
    grouped = tsframe.groupby([lambda x: x.year, lambda x: x.month])
    result = grouped.agg("mean")
    expected = grouped.mean()
    tm.assert_frame_equal(result, expected)

