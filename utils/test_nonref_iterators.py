
def test_nonref_iterators():
    pairs = m.IntPairs([(1, 2), (3, 4), (0, 5)])
    assert list(pairs.nonref()) == [(1, 2), (3, 4), (0, 5)]
    assert list(pairs.nonref_keys()) == [1, 3, 0]
    assert list(pairs.nonref_values()) == [2, 4, 5]

