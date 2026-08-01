
def test_groupby_aggregate_empty_with_multiindex_frame():
    # GH 39178
    df = DataFrame(columns=["a", "b", "c"])
    result = df.groupby(["a", "b"], group_keys=False).agg(d=("c", list))
    expected = DataFrame(
        columns=["d"], index=MultiIndex([[], []], [[], []], names=["a", "b"])
    )
    tm.assert_frame_equal(result, expected)

