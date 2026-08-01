
def test_merge_index_types(index):
    # gh-20777
    # assert key access is consistent across index types
    left = DataFrame({"left_data": [1, 2, 3]}, index=index)
    right = DataFrame({"right_data": [1.0, 2.0, 3.0]}, index=index)

    result = left.merge(right, on=["index_col"])

    expected = DataFrame(
        {"left_data": [1, 2, 3], "right_data": [1.0, 2.0, 3.0]}, index=index
    )
    tm.assert_frame_equal(result, expected)

