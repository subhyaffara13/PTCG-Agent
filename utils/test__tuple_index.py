
def test_Tuple_index():
    assert Tuple(4, 0, 1, 2, 3).index(4) == 0
    assert Tuple(0, 4, 1, 2, 3).index(4) == 1
    assert Tuple(0, 1, 4, 2, 3).index(4) == 2
    assert Tuple(0, 1, 2, 4, 3).index(4) == 3
    assert Tuple(0, 1, 2, 3, 4).index(4) == 4

    raises(ValueError, lambda: Tuple(0, 1, 2, 3).index(4))
    raises(ValueError, lambda: Tuple(4, 0, 1, 2, 3).index(4, 1))
    raises(ValueError, lambda: Tuple(0, 1, 2, 3, 4).index(4, 1, 4))

