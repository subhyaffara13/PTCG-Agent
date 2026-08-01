
def test_groupby_multiindex_missing_pair():
    # GH9049
    df = DataFrame(
        {
            "group1": ["a", "a", "a", "b"],
            "group2": ["c", "c", "d", "c"],
            "value": [1, 1, 1, 5],
        }
    )
    df = df.set_index(["group1", "group2"])
    df_grouped = df.groupby(level=["group1", "group2"], sort=True)

    res = df_grouped.agg("sum")
    idx = MultiIndex.from_tuples(
        [("a", "c"), ("a", "d"), ("b", "c")], names=["group1", "group2"]
    )
    exp = DataFrame([[2], [1], [5]], index=idx, columns=["value"])

    tm.assert_frame_equal(res, exp)

