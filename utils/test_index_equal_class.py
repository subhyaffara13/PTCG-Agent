
def test_index_equal_class(exact):
    idx1 = Index([0, 1, 2])
    idx2 = RangeIndex(3)

    tm.assert_index_equal(idx1, idx2, exact=exact)

