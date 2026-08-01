
def test_groupby_apply_none_first(in_data, out_idx, out_data):
    # GH 12824. Tests if apply returns None first.
    test_df1 = DataFrame(in_data)

    def test_func(x):
        if x.shape[0] < 2:
            return None
        return x.iloc[[0, -1]]

    result1 = test_df1.groupby("groups").apply(test_func)
    index1 = MultiIndex.from_arrays(out_idx, names=["groups", None])
    expected1 = DataFrame(out_data, index=index1)
    tm.assert_frame_equal(result1, expected1)

