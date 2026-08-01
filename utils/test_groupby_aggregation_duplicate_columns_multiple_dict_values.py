
def test_groupby_aggregation_duplicate_columns_multiple_dict_values():
    # GH#55041
    df = DataFrame(
        [[1, 2, 3, 4], [1, 3, 4, 5], [2, 4, 5, 6]],
        columns=["a", "b", "c", "c"],
    )
    gb = df.groupby("a")
    result = gb.agg({"c": ["sum", "min", "max", "min"]})

    expected = DataFrame(
        [[7, 3, 4, 3, 9, 4, 5, 4], [5, 5, 5, 5, 6, 6, 6, 6]],
        columns=MultiIndex(
            levels=[["c"], ["sum", "min", "max"]],
            codes=[[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 1, 0, 1, 2, 1]],
        ),
        index=Index([1, 2], name="a"),
    )
    tm.assert_frame_equal(result, expected)

