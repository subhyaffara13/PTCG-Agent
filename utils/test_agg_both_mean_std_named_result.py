
def test_agg_both_mean_std_named_result(cases, a_mean, b_std, agg):
    expected = pd.concat([a_mean, b_std], axis=1)
    result = cases.aggregate(**agg)
    tm.assert_frame_equal(result, expected, check_like=True)

