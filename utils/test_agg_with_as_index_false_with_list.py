
def test_agg_with_as_index_false_with_list():
    # GH#52849
    df = DataFrame({"a1": [0, 0, 1], "a2": [2, 3, 3], "b": [4, 5, 6]})
    gb = df.groupby(by=["a1", "a2"], as_index=False)
    result = gb.agg(["sum"])

    expected = DataFrame(
        data=[[0, 2, 4], [0, 3, 5], [1, 3, 6]],
        columns=MultiIndex.from_tuples([("a1", ""), ("a2", ""), ("b", "sum")]),
    )
    tm.assert_frame_equal(result, expected)

