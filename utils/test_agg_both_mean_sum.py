
def test_agg_both_mean_sum(cases, a_mean, a_sum, agg):
    expected = pd.concat([a_mean, a_sum], axis=1)
    expected.columns = ["mean", "sum"]
    result = cases["A"].aggregate(**agg)
    tm.assert_frame_equal(result, expected)

