
def test_join_overlapping_to_multiindex_with_same_interval(range_index, interval_index):
    #  GH-45661
    multi_index = MultiIndex.from_product([interval_index, range_index])
    result = interval_index.join(multi_index)

    tm.assert_index_equal(result, multi_index)

