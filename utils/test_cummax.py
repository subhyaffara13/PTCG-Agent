
def test_cummax(dtypes_for_minmax):
    dtype = dtypes_for_minmax[0]

    # GH 15048
    base_df = DataFrame({"A": [1, 1, 1, 1, 2, 2, 2, 2], "B": [3, 4, 3, 2, 2, 3, 2, 1]})
    expected_maxs = [3, 4, 4, 4, 2, 3, 3, 3]

    df = base_df.astype(dtype)

    expected = DataFrame({"B": expected_maxs}).astype(dtype)
    result = df.groupby("A").cummax()
    tm.assert_frame_equal(result, expected)
    result = df.groupby("A", group_keys=False).B.apply(lambda x: x.cummax()).to_frame()
    tm.assert_frame_equal(result, expected)

