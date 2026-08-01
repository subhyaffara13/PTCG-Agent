
def test_unit_propagate_int_repr():
    assert unit_propagate_int_repr([{1, 2}], 1) == []
    assert unit_propagate_int_repr(map(set,
        [[1, 2], [-1, 3], [-3, 2], [1]]), 1) == [{3}, {-3, 2}]

