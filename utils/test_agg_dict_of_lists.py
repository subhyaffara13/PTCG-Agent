
def test_agg_dict_of_lists(cases, a_mean, a_std, b_mean, b_std):
    expected = pd.concat([a_mean, a_std, b_mean, b_std], axis=1)
    expected.columns = pd.MultiIndex.from_tuples(
        [("A", "mean"), ("A", "std"), ("B", "mean"), ("B", "std")]
    )
    result = cases.aggregate({"A": ["mean", "std"], "B": ["mean", "std"]})
    tm.assert_frame_equal(result, expected, check_like=True)

