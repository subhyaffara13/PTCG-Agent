
def test_merge_antijoin_no_common_elements():
    left = DataFrame({"A": [1, 2, 3]})
    right = DataFrame({"B": [4, 5, 6]})

    result = merge(left, right, how="left_anti", left_on="A", right_on="B")
    expected = DataFrame({"A": [1, 2, 3], "B": [np.nan, np.nan, np.nan]})
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_on="A", right_on="B")
    expected = DataFrame({"A": [np.nan, np.nan, np.nan], "B": [4, 5, 6]})
    tm.assert_frame_equal(result, expected)

