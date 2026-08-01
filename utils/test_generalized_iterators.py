
def test_generalized_iterators():
    assert list(m.IntPairs([(1, 2), (3, 4), (0, 5)]).nonzero()) == [(1, 2), (3, 4)]
    assert list(m.IntPairs([(1, 2), (2, 0), (0, 3), (4, 5)]).nonzero()) == [(1, 2)]
    assert list(m.IntPairs([(0, 3), (1, 2), (3, 4)]).nonzero()) == []

    assert list(m.IntPairs([(1, 2), (3, 4), (0, 5)]).nonzero_keys()) == [1, 3]
    assert list(m.IntPairs([(1, 2), (2, 0), (0, 3), (4, 5)]).nonzero_keys()) == [1]
    assert list(m.IntPairs([(0, 3), (1, 2), (3, 4)]).nonzero_keys()) == []

    assert list(m.IntPairs([(1, 2), (3, 4), (0, 5)]).nonzero_values()) == [2, 4]
    assert list(m.IntPairs([(1, 2), (2, 0), (0, 3), (4, 5)]).nonzero_values()) == [2]
    assert list(m.IntPairs([(0, 3), (1, 2), (3, 4)]).nonzero_values()) == []

    # __next__ must continue to raise StopIteration
    it = m.IntPairs([(0, 0)]).nonzero()
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(it)

    it = m.IntPairs([(0, 0)]).nonzero_keys()
    for _ in range(3):
        with pytest.raises(StopIteration):
            next(it)

