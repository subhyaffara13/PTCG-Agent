
def test_pass_args_kwargs_dataframe(tsframe, as_index):
    def f(x, q=None, axis=0):
        return np.percentile(x, q, axis=axis)

    df_grouped = tsframe.groupby(lambda x: x.month, as_index=as_index)
    agg_result = df_grouped.agg(np.percentile, 80, axis=0)
    apply_result = df_grouped.apply(DataFrame.quantile, 0.8)
    expected = df_grouped.quantile(0.8)
    tm.assert_frame_equal(apply_result, expected, check_names=False)
    tm.assert_frame_equal(agg_result, expected)

    apply_result = df_grouped.apply(DataFrame.quantile, [0.4, 0.8])
    expected_seq = df_grouped.quantile([0.4, 0.8])
    if not as_index:
        # apply treats the op as a transform; .quantile knows it's a reduction
        apply_result.index = range(4)
        apply_result.insert(loc=0, column="level_0", value=[1, 1, 2, 2])
        apply_result.insert(loc=1, column="level_1", value=[0.4, 0.8, 0.4, 0.8])
    tm.assert_frame_equal(apply_result, expected_seq, check_names=False)

    agg_result = df_grouped.agg(f, q=80)
    apply_result = df_grouped.apply(DataFrame.quantile, q=0.8)
    tm.assert_frame_equal(agg_result, expected)
    tm.assert_frame_equal(apply_result, expected, check_names=False)

