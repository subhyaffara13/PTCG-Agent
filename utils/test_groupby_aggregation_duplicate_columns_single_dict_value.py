
def test_groupby_aggregation_duplicate_columns_single_dict_value():
    # GH#55041
    df = DataFrame(
        [[1, 2, 3, 4], [1, 3, 4, 5], [2, 4, 5, 6]],
        columns=["a", "b", "c", "c"],
    )
    gb = df.groupby("a")
    result = gb.agg({"c": "sum"})

    expected = DataFrame(
        [[7, 9], [5, 6]], columns=["c", "c"], index=Index([1, 2], name="a")
    )
    tm.assert_frame_equal(result, expected)

