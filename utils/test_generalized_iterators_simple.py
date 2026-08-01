
def test_generalized_iterators_simple():
    assert list(m.IntPairs([(1, 2), (3, 4), (0, 5)]).simple_iterator()) == [
        (1, 2),
        (3, 4),
        (0, 5),
    ]
    assert list(m.IntPairs([(1, 2), (3, 4), (0, 5)]).simple_keys()) == [1, 3, 0]
    assert list(m.IntPairs([(1, 2), (3, 4), (0, 5)]).simple_values()) == [2, 4, 5]

