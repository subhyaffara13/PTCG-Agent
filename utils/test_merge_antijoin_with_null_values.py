
def test_merge_antijoin_with_null_values():
    left = DataFrame({"A": [1.0, 2.0, None, 4.0]})
    right = DataFrame({"B": [2.0, None, 5.0]})

    result = merge(left, right, how="left_anti", left_on="A", right_on="B")
    expected = DataFrame({"A": [1.0, 4.0], "B": [np.nan, np.nan]}, index=[0, 3])
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_on="A", right_on="B")
    expected = DataFrame({"A": [np.nan], "B": [5.0]}, index=[2])
    tm.assert_frame_equal(result, expected)

