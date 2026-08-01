
def test_merge_upcasting_no_copy():
    left = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    left_copy = left.copy()
    right = DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]}, dtype=object)
    result = merge(left, right, on="a")
    assert np.shares_memory(get_array(result, "b"), get_array(left, "b"))
    assert not np.shares_memory(get_array(result, "a"), get_array(left, "a"))
    tm.assert_frame_equal(left, left_copy)

    result = merge(right, left, on="a")
    assert np.shares_memory(get_array(result, "b"), get_array(left, "b"))
    assert not np.shares_memory(get_array(result, "a"), get_array(left, "a"))
    tm.assert_frame_equal(left, left_copy)

