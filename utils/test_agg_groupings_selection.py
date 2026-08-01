
def test_agg_groupings_selection():
    # GH#51186 - a selected grouping should be in the output of agg
    df = DataFrame({"a": [1, 1, 2], "b": [3, 3, 4], "c": [5, 6, 7]})
    gb = df.groupby(["a", "b"])
    selected_gb = gb[["b", "c"]]
    result = selected_gb.agg(lambda x: x.sum())
    index = MultiIndex(
        levels=[[1, 2], [3, 4]], codes=[[0, 1], [0, 1]], names=["a", "b"]
    )
    expected = DataFrame({"b": [6, 4], "c": [11, 7]}, index=index)
    tm.assert_frame_equal(result, expected)

