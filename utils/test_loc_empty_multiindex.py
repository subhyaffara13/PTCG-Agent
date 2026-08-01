
def test_loc_empty_multiindex():
    # GH#36936
    arrays = [["a", "a", "b", "a"], ["a", "a", "b", "b"]]
    index = MultiIndex.from_arrays(arrays, names=("idx1", "idx2"))
    df = DataFrame([1, 2, 3, 4], index=index, columns=["value"])

    # loc on empty multiindex == loc with False mask
    empty_multiindex = df.loc[df.loc[:, "value"] == 0, :].index
    result = df.loc[empty_multiindex, :]
    expected = df.loc[[False] * len(df.index), :]
    tm.assert_frame_equal(result, expected)

    # replacing value with loc on empty multiindex
    df.loc[df.loc[df.loc[:, "value"] == 0].index, "value"] = 5
    result = df
    expected = DataFrame([1, 2, 3, 4], index=index, columns=["value"])
    tm.assert_frame_equal(result, expected)

