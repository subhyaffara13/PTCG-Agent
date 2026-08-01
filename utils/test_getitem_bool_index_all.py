
def test_getitem_bool_index_all(box):
    # GH#22533
    ind1 = box([True] * 5)
    idx = MultiIndex.from_tuples([(10, 1), (20, 2), (30, 3), (40, 4), (50, 5)])
    tm.assert_index_equal(idx[ind1], idx)

    ind2 = box([True, False, True, False, False])
    expected = MultiIndex.from_tuples([(10, 1), (30, 3)])
    tm.assert_index_equal(idx[ind2], expected)

