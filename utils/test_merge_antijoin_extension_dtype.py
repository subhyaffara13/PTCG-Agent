
def test_merge_antijoin_extension_dtype(dtype):
    left = DataFrame(
        {
            "join_col": [1, 3, 5],
            "left_val": [1, 2, 3],
        }
    )
    right = DataFrame(
        {
            "join_col": [2, 3, 4],
            "right_val": [1, 2, 3],
        }
    )
    left = left.astype({"join_col": dtype})
    right = right.astype({"join_col": dtype})
    result = merge(left, right, how="left_anti", on="join_col")
    expected = DataFrame(
        {
            "join_col": [1, 5],
            "left_val": [1, 3],
            "right_val": [np.nan, np.nan],
        },
        index=[0, 2],
    )
    expected = expected.astype({"join_col": dtype})
    tm.assert_frame_equal(result, expected)

