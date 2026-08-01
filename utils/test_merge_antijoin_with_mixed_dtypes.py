
def test_merge_antijoin_with_mixed_dtypes():
    left = DataFrame({"A": [1, "2", 3.0]})
    right = DataFrame({"B": ["2", 3.0, 4]})

    result = merge(left, right, how="left_anti", left_on="A", right_on="B")
    expected = DataFrame({"A": [1], "B": [np.nan]}, dtype=object)
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_on="A", right_on="B")
    expected = DataFrame({"A": [np.nan], "B": [4]}, dtype=object, index=[2])
    tm.assert_frame_equal(result, expected)

