
def test_find_pure_symbol_int_repr():
    assert find_pure_symbol_int_repr([1], [{1}]) == (1, True)
    assert find_pure_symbol_int_repr([1, 2],
                [{-1, 2}, {-2, 1}]) == (None, None)
    assert find_pure_symbol_int_repr([1, 2, 3],
                [{1, -2}, {-2, -3}, {3, 1}]) == (1, True)
    assert find_pure_symbol_int_repr([1, 2, 3],
                [{-1, 2}, {2, -3}, {3, 1}]) == (2, True)
    assert find_pure_symbol_int_repr([1, 2, 3],
                [{-1, -2}, {-2, -3}, {3, 1}]) == (2, False)
    assert find_pure_symbol_int_repr([1, 2, 3],
                [{-1, 2}, {-2, -3}, {3, 1}]) == (None, None)

