
def test_merge_ea(any_numeric_ea_dtype, join_type):
    # GH#44240
    left = DataFrame({"a": [1, 2, 3], "b": 1}, dtype=any_numeric_ea_dtype)
    right = DataFrame({"a": [1, 2, 3], "c": 2}, dtype=any_numeric_ea_dtype)
    result = left.merge(right, how=join_type)
    expected = DataFrame({"a": [1, 2, 3], "b": 1, "c": 2}, dtype=any_numeric_ea_dtype)
    tm.assert_frame_equal(result, expected)

