
def test_merge_indicator_no_deep_copy():
    left = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    right = DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})
    result = merge(left, right, on="a", indicator=True)
    assert np.shares_memory(get_array(result, "b"), get_array(left, "b"))
    assert np.shares_memory(get_array(result, "c"), get_array(right, "c"))

