
def test_merge_antijoin_same_df():
    left = DataFrame({"A": [1, 2, 3]}, index=["a", "b", "c"], dtype=np.int64)
    result = merge(left, left, how="left_anti", left_index=True, right_index=True)
    expected = DataFrame([], columns=["A_x", "A_y"], dtype=np.int64)
    tm.assert_frame_equal(result, expected, check_index_type=False)

