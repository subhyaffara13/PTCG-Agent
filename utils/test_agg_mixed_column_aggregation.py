
def test_agg_mixed_column_aggregation(cases, a_mean, a_std, b_mean, b_std, request):
    expected = pd.concat([a_mean, a_std, b_mean, b_std], axis=1)
    expected.columns = pd.MultiIndex.from_product([["A", "B"], ["mean", "<lambda_0>"]])
    # "date" is an index and a column, so get included in the agg
    if "df_mult" in request.node.callspec.id:
        date_mean = cases["date"].mean()
        date_std = cases["date"].std()
        expected = pd.concat([date_mean, date_std, expected], axis=1)
        expected.columns = pd.MultiIndex.from_product(
            [["date", "A", "B"], ["mean", "<lambda_0>"]]
        )
    result = cases.aggregate([np.mean, lambda x: np.std(x, ddof=1)])
    tm.assert_frame_equal(result, expected)

