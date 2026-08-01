
def test_merge_outer_with_NaN(dtype):
    # GH#43550
    item = np.nan if dtype is None else pd.NA
    left = DataFrame({"key": [1, 2], "col1": [1, 2]}, dtype=dtype)
    right = DataFrame({"key": [item, item], "col2": [3, 4]}, dtype=dtype)
    result = merge(left, right, on="key", how="outer")
    expected = DataFrame(
        {
            "key": [1, 2, item, item],
            "col1": [1, 2, item, item],
            "col2": [item, item, 3, 4],
        },
        dtype=dtype,
    )
    tm.assert_frame_equal(result, expected)

    # switch left and right
    result = merge(right, left, on="key", how="outer")
    expected = DataFrame(
        {
            "key": [1, 2, item, item],
            "col2": [item, item, 3, 4],
            "col1": [1, 2, item, item],
        },
        dtype=dtype,
    )
    tm.assert_frame_equal(result, expected)

