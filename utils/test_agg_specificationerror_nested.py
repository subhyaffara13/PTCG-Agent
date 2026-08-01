
def test_agg_specificationerror_nested(cases, cols, agg, a_sum, a_std, b_mean, b_std):
    # agg with different hows
    # equivalent of using a selection list / or not
    expected = pd.concat([a_sum, a_std, b_mean, b_std], axis=1)
    expected.columns = pd.MultiIndex.from_tuples(
        [("A", "sum"), ("A", "std"), ("B", "mean"), ("B", "std")]
    )
    if cols is not None:
        obj = cases[cols]
    else:
        obj = cases

    result = obj.agg(agg)
    tm.assert_frame_equal(result, expected, check_like=True)

