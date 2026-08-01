
def test_string_rank_grouping():
    # GH 19354
    df = DataFrame({"A": [1, 1, 2], "B": [1, 2, 3]})
    result = df.groupby("A").transform("rank")
    expected = DataFrame({"B": [1.0, 2.0, 1.0]})
    tm.assert_frame_equal(result, expected)

