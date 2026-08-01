
def test_slice_indexer_with_missing_value(index_arr, expected, start_idx, end_idx):
    # issue 19132
    idx = MultiIndex.from_arrays(index_arr)
    result = idx.slice_indexer(start=start_idx, end=end_idx)
    assert result == expected

