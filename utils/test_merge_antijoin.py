
def test_merge_antijoin():
    # GH#42916
    left = DataFrame({"A": [1, 2, 3]}, index=["a", "b", "c"])
    right = DataFrame({"B": [1, 2, 4]}, index=["a", "b", "d"])

    result = merge(left, right, how="left_anti", left_index=True, right_index=True)
    expected = DataFrame({"A": [3], "B": [np.nan]}, index=["c"])
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_index=True, right_index=True)
    expected = DataFrame({"A": [np.nan], "B": [4]}, index=["d"])
    tm.assert_frame_equal(result, expected)

