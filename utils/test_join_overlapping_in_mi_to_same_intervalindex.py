
def test_join_overlapping_in_mi_to_same_intervalindex(range_index, interval_index):
    #  GH-45661
    multi_index = MultiIndex.from_product([interval_index, range_index])
    result = multi_index.join(interval_index)

    tm.assert_index_equal(result, multi_index)

