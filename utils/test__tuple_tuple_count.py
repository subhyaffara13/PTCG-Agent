
def test_Tuple_tuple_count():
    assert Tuple(0, 1, 2, 3).tuple_count(4) == 0
    assert Tuple(0, 4, 1, 2, 3).tuple_count(4) == 1
    assert Tuple(0, 4, 1, 4, 2, 3).tuple_count(4) == 2
    assert Tuple(0, 4, 1, 4, 2, 4, 3).tuple_count(4) == 3

