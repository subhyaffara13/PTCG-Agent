
def test_get_slice_bound_with_missing_value(index_arr, expected, target, algo):
    # issue 19132
    idx = MultiIndex.from_arrays(index_arr)
    result = idx.get_slice_bound(target, side=algo)
    assert result == expected

