
def test_groupby_aggregate_empty_key(kwargs):
    # GH: 32580
    df = DataFrame({"a": [1, 1, 2], "b": [1, 2, 3], "c": [1, 2, 4]})
    result = df.groupby("a").agg(kwargs)
    expected = DataFrame(
        [1, 4],
        index=Index([1, 2], dtype="int64", name="a"),
        columns=MultiIndex.from_tuples([["c", "min"]]),
    )
    tm.assert_frame_equal(result, expected)

