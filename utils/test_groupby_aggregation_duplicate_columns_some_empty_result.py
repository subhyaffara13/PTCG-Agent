
def test_groupby_aggregation_duplicate_columns_some_empty_result():
    # GH#55041
    df = DataFrame(
        [
            [1, 9843, 43, 54, 7867],
            [2, 940, 9, -34, 44],
            [1, -34, -546, -549358, 0],
            [2, 244, -33, -100, 44],
        ],
        columns=["a", "b", "b", "c", "c"],
    )
    gb = df.groupby("a")
    result = gb.agg({"b": [], "c": ["var"]})

    expected = DataFrame(
        [[1.509268e11, 30944844.5], [2.178000e03, 0.0]],
        columns=MultiIndex(levels=[["c"], ["var"]], codes=[[0, 0], [0, 0]]),
        index=Index([1, 2], name="a"),
    )
    tm.assert_frame_equal(result, expected)

