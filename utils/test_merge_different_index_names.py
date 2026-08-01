
def test_merge_different_index_names():
    # GH#45094
    left = DataFrame({"a": [1]}, index=Index([1], name="c"))
    right = DataFrame({"a": [1]}, index=Index([1], name="d"))
    result = merge(left, right, left_on="c", right_on="d")
    expected = DataFrame({"a_x": [1], "a_y": 1})
    tm.assert_frame_equal(result, expected)

