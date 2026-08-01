
def test_agg_multiple_mixed():
    # GH 20909
    mdf = DataFrame(
        {
            "A": [1, 2, 3],
            "B": [1.0, 2.0, 3.0],
            "C": ["foo", "bar", "baz"],
        }
    )
    expected = DataFrame(
        {
            "A": [1, 6],
            "B": [1.0, 6.0],
            "C": ["bar", "foobarbaz"],
        },
        index=["min", "sum"],
    )
    # sorted index
    result = mdf.agg(["min", "sum"])
    tm.assert_frame_equal(result, expected)

    result = mdf[["C", "B", "A"]].agg(["sum", "min"])
    # GH40420: the result of .agg should have an index that is sorted
    # according to the arguments provided to agg.
    expected = expected[["C", "B", "A"]].reindex(["sum", "min"])
    tm.assert_frame_equal(result, expected)

