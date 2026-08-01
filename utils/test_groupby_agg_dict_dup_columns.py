
def test_groupby_agg_dict_dup_columns():
    # GH#55006
    df = DataFrame(
        [[1, 2, 3, 4], [1, 3, 4, 5], [2, 4, 5, 6]],
        columns=["a", "b", "c", "c"],
    )
    gb = df.groupby("a")
    result = gb.agg({"b": "sum"})
    expected = DataFrame({"b": [5, 4]}, index=Index([1, 2], name="a"))
    tm.assert_frame_equal(result, expected)

