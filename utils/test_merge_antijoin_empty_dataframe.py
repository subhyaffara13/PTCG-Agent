
def test_merge_antijoin_empty_dataframe():
    left = DataFrame({"A": [], "B": []})
    right = DataFrame({"C": [], "D": []})

    result = merge(left, right, how="left_anti", left_on="A", right_on="C")
    expected = DataFrame({"A": [], "B": [], "C": [], "D": []})
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_on="A", right_on="C")
    tm.assert_frame_equal(result, expected)

