
def test_groupby_empty_multi_column(as_index, numeric_only):
    # GH 15106 & GH 41998
    df = DataFrame(data=[], columns=["A", "B", "C"])
    gb = df.groupby(["A", "B"], as_index=as_index)
    result = gb.sum(numeric_only=numeric_only)
    if as_index:
        index = MultiIndex([[], []], [[], []], names=["A", "B"])
        columns = ["C"] if not numeric_only else Index([], dtype="str")
    else:
        index = RangeIndex(0)
        columns = ["A", "B", "C"] if not numeric_only else ["A", "B"]
    expected = DataFrame([], columns=columns, index=index)
    tm.assert_frame_equal(result, expected)

