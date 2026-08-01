
def test_cummax_min_value_for_dtype(dtypes_for_minmax):
    dtype = dtypes_for_minmax[0]
    max_val = dtypes_for_minmax[2]

    # GH 15048
    base_df = DataFrame({"A": [1, 1, 1, 1, 2, 2, 2, 2], "B": [3, 4, 3, 2, 2, 3, 2, 1]})
    expected_maxs = [3, 4, 4, 4, 2, 3, 3, 3]

    df = base_df.astype(dtype)
    df.loc[[2, 6], "B"] = max_val
    expected = DataFrame({"B": expected_maxs}).astype(dtype)
    expected.loc[[2, 3, 6, 7], "B"] = max_val
    result = df.groupby("A").cummax()
    tm.assert_frame_equal(result, expected)
    expected = (
        df.groupby("A", group_keys=False).B.apply(lambda x: x.cummax()).to_frame()
    )
    tm.assert_frame_equal(result, expected)

